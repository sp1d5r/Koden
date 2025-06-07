from typing import Optional
from sqlmodel import Field
from .base import TimestampModel

class User(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    firebase_uid: str = Field(unique=True, index=True) 