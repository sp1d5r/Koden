from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Base user model with common attributes."""
    email: EmailStr
    name: str

class UserCreate(UserBase):
    """Model for creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Model for updating a user."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class UserResponse(UserBase):
    """Model for user responses."""
    id: int
    firebase_uid: str

    class Config:
        from_attributes = True  # Allows ORM model to be converted to Pydantic model

class UserListResponse(BaseModel):
    """Model for list of users response."""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int
