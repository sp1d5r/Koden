from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Literal
from datetime import datetime
from sqlalchemy import String, CheckConstraint
from .repos import Repo

# For type hints in Python code
TaskStatus = Literal["pending", "processing", "completed", "failed"]

class Task(SQLModel, table=True):
    """Base model for tracking background tasks."""
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: str  # Celery task ID
    status: str = Field(
        default="pending",
        sa_type=String(20),
        sa_column_kwargs={
            "nullable": False,
            "server_default": "pending"
        }
    )
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed')",
            name="valid_task_status"
        ),
    )

class RepoDownloadTask(SQLModel, table=True):
    """Model for tracking repository download tasks."""
    __tablename__ = "repo_download_tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: str  # Celery task ID
    status: str = Field(
        default="pending",
        sa_type=String(20),
        sa_column_kwargs={
            "nullable": False,
            "server_default": "pending"
        }
    )
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    repo_id: int = Field(foreign_key="repo.id")
    repo: "Repo" = Relationship(back_populates="download_tasks")

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed')",
            name="valid_repo_download_task_status"
        ),
    ) 