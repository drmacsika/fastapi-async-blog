from typing import Dict

from core.settings import settings
from core.test_utils import random_email, random_lower_string
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.crud import user
from accounts.schemas import UserCreate


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["active"] is True
    assert current_user["admin"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["active"] is True
    assert current_user["admin"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 201 <= r.status_code < 300
    created_user = r.json()
    u = user.get(db, email=username)
    assert u
    assert u.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    u = user.create(db, obj_in=user_in)
    user_id = u.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 201 <= r.status_code < 300
    api_user = r.json()
    existing_user = user.get(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
