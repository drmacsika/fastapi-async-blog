from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

"""Base fields for blog post category."""
class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    
"""Fields for creating blog post category."""
class CreateCategory(CategoryBase):
    ...
    
"""Fields for updating blog post category."""
class UpdateCategory(CategoryBase):
    post_id: int
    slug: str
    active: bool
    created: datetime

"""Response for blog post category."""
class Category(CategoryBase):
    id: int
    post_id: Optional[int] = None
    slug: str
    active: bool
    created: datetime
    updated: datetime
    
    class Config:
        orm_mode = True

"""Base fields for blog posts."""
class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    intro: Optional[str] = None
    content: Optional[str] = ...
    categories: List[Category] = None

"""Fields for creating blog post."""
class CreatePost(PostBase):
    ...

"""Fields for updating blog post."""
class UpdatePost(PostBase):
    slug: Optional[str] = None
    read_length: int
    view_count: int
    active: bool
    updated: datetime

"""Response for blog post."""
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




