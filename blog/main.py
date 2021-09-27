from fastapi import APIRouter

from blog import schemas

router = APIRouter()


@router.get("/blog")
async def blog():
    return {
        "detail": "Post executed successfully"
    }

@router.post("/blog/create")
async def create_post(request: schemas.Post) -> str:
    return request
