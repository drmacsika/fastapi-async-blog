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

@router.post("/login/access-token/", response_model=Token)
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

@router.post("/login/test-token/", response_model=UserOut)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}/", response_model=Message)
async def recover_password(email: str, db: AsyncSession = Depends(get_session)) -> Any:
    """
    Get a token to recover a lost or forgotten password.
    """
    u = await user.get(db=db, email=email)
    if not u:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=u.email, email=email, token=password_reset_token
    )
    return {"message": "Password recovery email sent"}


@router.post("/reset-password/", response_model=Message)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    confirm_password: str = Body(...),
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Reset a password after getting a password recovery token.
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    u = await user.get(db=db, email=email)
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if not u:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist.",
        )
    elif not user.is_active(u):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    u.password = hashed_password
    db.add(user)
    db.commit()
    return {"message": "Password updated successfully"}
