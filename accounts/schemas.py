from datetime import datetime
from typing import List

from blog.models import Post
from pydantic import BaseModel, EmailStr

"""Base fields for user."""
class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    
"""Base fields for creating a new user."""
class UserCreate(UserBase):
    password: str
    
"""Base fields for updating old user details user."""
class UserUpdate(BaseModel):
    name: str
    username: str
    active: bool = False

"""Base fields for user response."""
class User(UserBase):
    id: int
    articles: List[Post] = []
    staff: bool = False
    admin: bool = False
    active: bool = False
    created: datetime
    updated: datetime
    
    class Config:
        orm_mode = True

"""Base fields for entering user details in the database."""
class UserInDB(User):
    password: str
