from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class RepoBase(BaseModel):
    """Base repo model with common attributes."""
    name: str
    github_url: HttpUrl
    branch: Optional[str] = "main"

class RepoCreate(RepoBase):
    """Model for creating a new repo."""
    pass

class RepoUpdate(BaseModel):
    """Model for updating a repo."""
    name: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    branch: Optional[str] = None

class RepoResponse(RepoBase):
    """Model for repo responses."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows ORM model to be converted to Pydantic model

class RepoListResponse(BaseModel):
    """Model for list of repos with pagination."""
    repos: List[RepoResponse]
    total: int
    skip: int
    limit: int 