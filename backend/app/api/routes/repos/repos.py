from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from app.core.database import get_session
from app.core.dependencies import get_current_db_user
from db.models.user import User
from db.models.repos import Repo
from app.models.api.repos import RepoCreate, RepoUpdate, RepoResponse, RepoListResponse

router = APIRouter()

@router.post("/", response_model=RepoResponse, status_code=status.HTTP_201_CREATED)
async def create_repo(
    repo: RepoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_db_user)
):
    """Create a new repo for the current user."""
    # Check if repo already exists for this user
    existing_repo = session.exec(
        select(Repo)
        .where(Repo.user_id == current_user.id)
        .where(Repo.github_url == str(repo.github_url))
    ).first()
    
    if existing_repo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This repository is already being tracked"
        )

    db_repo = Repo(
        name=repo.name,
        github_url=str(repo.github_url),
        branch=repo.branch,
        user_id=current_user.id,
    )

    session.add(db_repo)
    session.commit()
    session.refresh(db_repo)
    return db_repo

@router.get("/", response_model=RepoListResponse)
async def read_repos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_db_user)
):
    """Get all repos for the current user with pagination."""
    repos = session.exec(
        select(Repo)
        .where(Repo.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    ).all()
    
    total = session.exec(
        select(func.count()).select_from(Repo).where(Repo.user_id == current_user.id)
    ).first()
    
    return RepoListResponse(
        repos=repos,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{repo_id}", response_model=RepoResponse)
async def read_repo(
    repo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_db_user)
):
    """Get a specific repo by ID."""
    repo = session.get(Repo, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repo not found"
        )
    
    # Check if the repo belongs to the current user
    if repo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this repo"
        )
    
    return repo

@router.patch("/{repo_id}", response_model=RepoResponse)
async def update_repo(
    repo_id: int,
    repo_update: RepoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_db_user)
):
    """Update a repo."""
    repo = session.get(Repo, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repo not found"
        )
    
    # Check if the repo belongs to the current user
    if repo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this repo"
        )
    
    # Update repo fields
    update_data = repo_update.model_dump(exclude_unset=True)
    if "github_url" in update_data:
        update_data["github_url"] = str(update_data["github_url"])
    
    for key, value in update_data.items():
        setattr(repo, key, value)
    
    session.add(repo)
    session.commit()
    session.refresh(repo)
    return repo

@router.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_repo(
    repo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_db_user)
):
    """Delete a repo."""
    repo = session.get(Repo, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repo not found"
        )
    
    # Check if the repo belongs to the current user
    if repo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this repo"
        )
    
    session.delete(repo)
    session.commit()
    return None 