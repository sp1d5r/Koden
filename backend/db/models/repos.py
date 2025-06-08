from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# Repo table
class Repo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    github_url: str
    branch: Optional[str] = "main"
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="repos")
    # analysis_jobs: List["AnalysisJob"] = Relationship(back_populates="repo")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)