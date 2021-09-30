from datetime import datetime
from typing import List

from blog.models import Post
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str
    
    
class UserUpdate(BaseModel):
    name: str
    username: str
    active: bool = False


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


class UserInDB(User):
    password: str
