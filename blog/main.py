from fastapi import APIRouter

router = APIRouter()

    


@router.post("/blog")
async def blog():
    return {"User": "Name"}
