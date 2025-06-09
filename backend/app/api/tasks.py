from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from db.models.tasks import Task, RepoDownloadTask, Repo
from app.services.task_service import TaskService
from app.core.auth import get_current_user
from app.core.database import get_session
from app.core.logging import logger
from app.celery_app import celery_app
from app.tasks.github import download_github_repo
from urllib.parse import urlparse

router = APIRouter()

def parse_github_url(url: str) -> tuple[str, str]:
    """Parse GitHub URL to get owner and repo name."""
    # Handle both https://github.com/owner/repo and https://github.com/owner/repo.git
    path = urlparse(url).path.strip('/')
    if path.endswith('.git'):
        path = path[:-4]
    parts = path.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid GitHub URL format: {url}")
    return parts[0], parts[1]

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get a task by its ID."""
    task_service = TaskService(db)
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.get("/repos/{repo_id}/download-tasks", response_model=List[RepoDownloadTask])
async def get_repo_download_tasks(
    repo_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all download tasks for a repository."""
    task_service = TaskService(db)
    return task_service.get_repo_download_tasks(repo_id)

@router.post("/repos/{repo_id}/download", response_model=RepoDownloadTask)
async def create_repo_download_task(
    repo_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create a new repository download task."""
    task_service = TaskService(db)
    
    # Get repo details from the database
    repo = db.get(Repo, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    try:
        # Parse GitHub URL to get owner and repo name
        owner, repo_name = parse_github_url(repo.github_url)
        logger.info(f"Creating download task for {owner}/{repo_name}")
        
        # Create Celery task with explicit queue
        celery_task = download_github_repo.apply_async(
            args=[owner, repo_name, repo.branch or "main", current_user.get("github_access_token")],
            queue='default',
            routing_key='default'
        )
        logger.info(f"Celery task created with ID: {celery_task.id}")
        
        # Create task record in database
        task = task_service.create_download_task(repo_id, celery_task.id)
        logger.info(f"Database task record created: {task}")
        
        # Verify task is in Redis
        task_in_redis = celery_app.AsyncResult(celery_task.id)
        logger.info(f"Task in Redis status: {task_in_redis.status}, ready: {task_in_redis.ready()}")
        
        # Check if task is in the queue
        i = celery_app.control.inspect()
        active = i.active()
        reserved = i.reserved()
        scheduled = i.scheduled()
        logger.info(f"Task queues status - Active: {active}, Reserved: {reserved}, Scheduled: {scheduled}")
        
        return task
    except ValueError as e:
        logger.error(f"Invalid GitHub URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating download task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create download task"
        )

@router.get("/{task_id}/status")
async def get_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get the current status of a task."""
    task_service = TaskService(db)
    
    # Get task from database
    task = task_service.get_task(task_id)
    logger.info(f"Task status from DB: {task}")
    
    # Get Celery task status
    celery_task = celery_app.AsyncResult(task_id)
    logger.info(f"Celery task status: {celery_task.status}, ready: {celery_task.ready()}, result: {celery_task.result}")
    
    # Map Celery states to our states
    celery_status_map = {
        'PENDING': 'pending',
        'STARTED': 'processing',
        'SUCCESS': 'completed',
        'FAILURE': 'failed',
        'RETRY': 'processing',
        'REVOKED': 'failed'
    }
    celery_status = celery_status_map.get(celery_task.status, 'failed')
    
    # If task doesn't exist in DB but exists in Redis
    if not task and celery_status != 'pending':
        # Create task record in database
        task = task_service.create_download_task(
            repo_id=0,  # We don't know the repo_id at this point
            task_id=task_id,
            status=celery_status,
            output_path=celery_task.result if celery_status == "completed" else None,
            error_message=str(celery_task.result) if celery_status == "failed" else None
        )
        logger.info(f"Created missing task record: {task}")
    elif not task:
        # Task doesn't exist in either place
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # If task exists in Redis/Celery but status has changed
    if celery_status != task.status:
        logger.info(f"Updating task status from {task.status} to {celery_status}")
        updated_task = task_service.update_task_status(
            task_id=task_id,
            status=celery_status,
            output_path=celery_task.result if celery_status == "completed" else None,
            error_message=str(celery_task.result) if celery_status == "failed" else None
        )
        if updated_task:
            task = updated_task
            logger.info(f"Updated task status: {task}")
    
    return {
        "status": task.status,
        "output_path": task.output_path,
        "error_message": task.error_message
    }

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete a task and its associated Celery task."""
    task_service = TaskService(db)
    
    # First try to find it in repo_download_tasks
    task = db.query(RepoDownloadTask).filter(RepoDownloadTask.task_id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    try:
        # Try to revoke the Celery task if it's still running
        celery_task = celery_app.AsyncResult(task_id)
        if celery_task.state in ['PENDING', 'STARTED']:
            celery_app.control.revoke(task_id, terminate=True)
            logger.info(f"Revoked Celery task {task_id}")
        
        # Delete the task from the database
        db.delete(task)
        db.commit()
        logger.info(f"Deleted task {task_id} from database")
        
        return {"message": "Task deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        ) 