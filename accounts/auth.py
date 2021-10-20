from typing import Any

from core.dependencies import get_current_user, get_session
from core.utils import (generate_password_reset_token, get_password_hash,
                        send_reset_password_email, verify_password_reset_token)
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.auth_schemas import Message, Token
from accounts.crud import user
from accounts.models import User
from accounts.schemas import UserOut

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return await user.authenticate(
        email=form_data.username,
        password=form_data.password, 
        db=db
    )

@router.post("/login/test-token", response_model=UserOut)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user



