from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator

"""Base fields for blog posts."""
class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    intro: Optional[str] = None
    content: Optional[str] = ...
    category_id: Optional[int] = None
    # categories: List[CategoryOut] = None

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
class PostOut(BaseModel):
    id: int
    slug: str
    read_length: int
    view_count: int
    active: bool
    created: datetime
    updated: datetime
    
    class Config:
        orm_mode = True


"""Base fields for blog post category."""
class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    
    @validator("title")
    def check_title_availability(cls, value):
        if value == "":
            raise ValueError('Title cannot be empty.')
        return value
    
    
"""Fields for creating blog post category."""
class CreateCategory(CategoryBase):
    ...
    
"""Fields for updating blog post category."""
class UpdateCategory(CategoryBase):
    slug: str
    active: bool
    
    @validator("slug")
    def check_slug_availability(cls, slg):
        if slg == "":
            raise ValueError('Slug cannot be empty.')
        return slg
    

"""Response for blog post category."""
class CategoryOut(CategoryBase):
    id: int
    slug: str
    active: bool
    # post: List[PostOut] = []
    updated: datetime
    
    class Config:
        orm_mode = True


