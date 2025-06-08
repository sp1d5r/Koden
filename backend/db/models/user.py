from typing import Optional, List
from sqlmodel import Field, Relationship
from .base import TimestampModel
from .repos import Repo
class User(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    firebase_uid: str = Field(unique=True, index=True) 
    repos: List["Repo"] = Relationship(back_populates="user")