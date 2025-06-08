from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.auth import get_current_user
from db.models.user import User

async def get_current_db_user(
    session: Session = Depends(get_session),
    firebase_user: dict = Depends(get_current_user)
) -> User:
    """Get the current user from the database using firebase_uid."""
    user = session.exec(
        select(User).where(User.firebase_uid == firebase_user["uid"])
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    return user 