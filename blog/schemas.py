from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    

class CreateCategory(CategoryBase):
    ...


class Category(CategoryBase):
    id: int
    post_id: int
    slug: str
    active: bool
    created: datetime
    updated: datetime
    
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    intro: Optional[str] = None
    content: Optional[str] = ...
    categories: List[Category] = None

class CreatePost(PostBase):
    ...

class Post(BaseModel):
    id: int
    slug: str
    read_length: int
    view_count: int
    active: bool
    created: datetime
    updated: datetime
    
    class Config:
        orm_mode = True
