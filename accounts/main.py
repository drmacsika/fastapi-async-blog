from typing import Any, List

from core.dependencies import (get_current_active_superuser,
                               get_current_active_user, get_session)
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.crud import user
from accounts.models import User
from accounts.schemas import UserCreate, UserUpdate

router = APIRouter()

    
@router.get("/users/", response_model=List[User])
async def get_all_users(
    db: AsyncSession = Depends(get_session),
    limit: int = 100, offset: int = 0,
    current_user: User = Depends(get_current_active_superuser)) -> Any:
    """Return all users."""
    return await user.get_multiple(db=db, offset=offset, limit=limit)
    

@router.post("/users/", response_model=User, status_code=201)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)) -> Any:
    """
    Create new user.
    """
    return await user.create(obj_in=user_in, db=db)

    

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: AsyncSession = Depends(get_session),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    return current_user
    
    
    
    
    
    
    
    

