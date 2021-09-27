from fastapi import APIRouter

from blog.models import (Category_Pydantic, CategoryIn_Pydantic, Post_Pydantic,
                         PostIn_Pydantic)

router = APIRouter()

    


@router.post("/signup/", response_model=Post_Pydantic)
async def signup(user: PostIn_Pydantic):
    
    return {"User": "Name"}
