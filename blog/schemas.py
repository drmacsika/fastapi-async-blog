from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    intro: Optional[str] = None
    content: Optional[str] = ...

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
