from typing import List
from db.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User,
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
):
    """Create a new user."""
    # Check if user with email already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Set the Firebase UID
    user.firebase_uid = firebase_user["uid"]
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
):
    """Get all users with pagination."""
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@router.get("/me", response_model=User)
async def read_current_user(
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
):
    """Get the current user's profile."""
    user = session.exec(
        select(User).where(User.firebase_uid == firebase_user["uid"])
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    return user

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
):
    """Get a specific user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: User,
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
):
    """Update a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if the user is updating their own profile
    if user.firebase_uid != firebase_user["uid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    # Check if email is being updated and if it's already taken
    if user_update.email != user.email:
        existing_user = session.exec(
            select(User).where(User.email == user_update.email)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user fields
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
):
    """Delete a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if the user is deleting their own profile
    if user.firebase_uid != firebase_user["uid"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    
    session.delete(user)
    session.commit()
    return None

