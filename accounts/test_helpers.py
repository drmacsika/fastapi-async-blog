from typing import Dict

from core.settings import settings
from core.test_utils import random_email, random_lower_string
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.crud import user
from accounts.models import User
from accounts.schemas import UserCreate, UserUpdate


def user_authentication_headers(
    *, client: TestClient, 
    email: str, password: str) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    first_name = random_lower_string()
    last_name = random_lower_string()
    user_in = UserCreate(
        username=email,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    return await user.create(db=db, obj_in=user_in)


async def authentication_token_from_email(
    *, client: TestClient, 
    email: str, db: AsyncSession) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    first_name = random_lower_string()
    last_name = random_lower_string()
    
    u = await user.get(email=email, db=db)
    if not u:
        user_in_create = UserCreate(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password)
        u = await user.create(db=db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        u = user.update(obj_in=user_in_update, db=db, slug_field=email)
    return user_authentication_headers(
        client=client, 
        email=email, 
        password=password
    )
