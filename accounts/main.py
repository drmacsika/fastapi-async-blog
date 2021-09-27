from fastapi import APIRouter

from accounts.models import UserIn_Pydantic, UserOut_Pydantic

router = APIRouter()

    


@router.post("/signup/", response_model=UserOut_Pydantic)
async def signup(user: UserIn_Pydantic):
    
    return {"User": "Name"}
