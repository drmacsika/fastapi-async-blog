from datetime import datetime
from typing import List, Optional

from blog.models import Post
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base fields for user.
    """
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    staff: bool = False
    admin: bool = False
    active: bool = False
    
    
class UserCreate(UserBase):
    """
    Base fields for creating a new user.
    """
    password: str
    
    
class UserUpdate(UserBase):
    """
    Base fields for updating old user details user.
    """
    password: Optional[str] = None
    active: bool = False


class User(UserBase):
    """
    Base fields for user response.
    """
    id: int
    # articles: List[Post] = []
    created: datetime
    updated: datetime
    
    class Config:
        orm_mode = True


class UserInDB(User):
    """
    Base fields for entering user details in the database.
    """
    password: str
