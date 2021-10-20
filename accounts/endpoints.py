from typing import Any, List

from core.dependencies import (get_current_active_superuser,
                               get_current_active_user, get_session)
from core.settings import settings
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.crud import user
from accounts.models import User
from accounts.schemas import UserCreate, UserOut, UserUpdate

router = APIRouter()

    
@router.get("/users/", response_model=List[UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_session),
    limit: int = 100, offset: int = 0,
    current_user: User = Depends(get_current_active_superuser)) -> Any:
    """Return all users."""
    return await user.get_multiple(db=db, offset=offset, limit=limit)
    

@router.post("/users/", response_model=UserOut, status_code=201)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)) -> Any:
    """
    Create new user.
    """
    return await user.create(obj_in=user_in, db=db)

    

@router.put("/me/", response_model=UserOut)
async def update_user_me(
    db: AsyncSession = Depends(get_session),
    first_name: str = Body(None),
    last_name: str = Body(None),
    username: str = Body(None),
    email: EmailStr = Body(None),
    password: str = Body(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if username is not None:
        user_in.username = username
    if email is not None:
        user_in.email = email
    return await user.update(obj_in=user_in, db=db, slug_field=current_user)
    
    
@router.get("/me/", response_model=UserOut)
def read_user_me(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open/", response_model=UserOut)
async def create_user_open(
    request: UserCreate,
    db: AsyncSession = Depends(get_session)
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    return await user.create(obj_in=request, db=db)    
    

@router.get("/{user_id}/", response_model=UserOut)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Get a specific user by id.
    """
    await user.get_by_id(id=user_id, db=db)
    if user == current_user:
        return user
    if not user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}/", response_model=UserOut)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Update a user.
    """
    u = await user.get_by_id(id=user_id, db=db)
    if not u:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await user.update(db, db_obj=user, obj_in=user_in)
    return user

