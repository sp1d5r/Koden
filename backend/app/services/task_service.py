from typing import Optional, List
from sqlmodel import Session, select
from db.models.tasks import Task, RepoDownloadTask, TaskStatus
from db.models.repos import Repo
from app.core.logging import logger

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_download_task(self, repo_id: int, task_id: str) -> RepoDownloadTask:
        """Create a new repository download task."""
        task = RepoDownloadTask(
            repo_id=repo_id,
            task_id=task_id,
            status="pending"
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by its Celery task ID."""
        return self.db.exec(
            select(Task).where(Task.task_id == task_id)
        ).first()

    def get_repo_download_tasks(self, repo_id: int) -> List[RepoDownloadTask]:
        """Get all download tasks for a repository."""
        return self.db.exec(
            select(RepoDownloadTask)
            .where(RepoDownloadTask.repo_id == repo_id)
            .order_by(RepoDownloadTask.created_at.desc())
        ).all()

    def update_task_status(
        self, 
        task_id: str, 
        status: TaskStatus, 
        output_path: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Optional[Task]:
        """Update a task's status and optional output/error information."""
        task = self.get_task(task_id)
        if task:
            task.status = status
            if output_path:
                task.output_path = output_path
            if error_message:
                task.error_message = error_message
            self.db.commit()
 