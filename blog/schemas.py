from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: Optional[str] = None
    intro: Optional[str] = None

class CreatePost(PostBase):
    ...

class Post(BaseModel):
    id: int
    
    class Config:
        orm_mode = True



