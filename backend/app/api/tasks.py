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
        
        # Create Celery task
        celery_task = download_github_repo.delay(
            owner=owner,
            repo=repo_name,
            ref=repo.branch or "main",
            access_token=current_user.get("github_access_token")
        )
        
        # Create task record in database
        task = task_service.create_download_task(repo_id, celery_task.id)
        return task
    except ValueError as e:
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

@router.get("/tasks/{task_id}/status")
async def get_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get the current status of a task."""
    task_service = TaskService(db)
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Get Celery task status
    celery_task = celery_app.AsyncResult(task_id)
    celery_status = celery_task.status
    
    # Update task status in database if it has changed
    if celery_status != task.status:
        task_service.update_task_status(
            task_id=task_id,
            status=celery_status,
            output_path=celery_task.result if celery_status == "completed" else None,
            error_message=str(celery_task.result) if celery_status == "failed" else None
        )
        task = task_service.get_task(task_id)
    
    return {
        "status": task.status,
        "output_path": task.output_path,
        "error_message": task.error_message
    } 