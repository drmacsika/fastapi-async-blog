from core.settings import settings
from core.utils import unique_slug_generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from blog.test_helpers import create_random_category, create_random_post

test_data = {
        "title": "Archangel",
        "description": "macsika"
    }

def test_create_post(
        client: TestClient,
        superuser_token_headers: dict,
        db: AsyncSession
    ) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/blog/posts/",
        headers=superuser_token_headers,
        json=test_data
    )
    assert response.status_code == 201 or response.status_code == 200
    content = response.json()
    assert content["title"] == test_data["title"]
    assert content["description"] == test_data["description"]
    assert content["slug"] == unique_slug_generator(test_data["title"])
    assert "id" in content
    assert "owner_id" in content


def test_create_category(
        client: TestClient,
        superuser_token_headers: dict,
        db: AsyncSession
    ) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/blog/tags/",
        headers=superuser_token_headers,
        json=test_data
    )
    assert response.status_code == 201 or response.status_code == 200
    content = response.json()
    assert content["title"] == test_data["title"]
    assert content["description"] == test_data["description"]
    assert content["slug"] == unique_slug_generator(test_data["title"])
    assert "id" in content


def test_read_post(
    client: TestClient,
    superuser_token_headers: dict,
    db: AsyncSession) -> None:
    item = create_random_post(db)
    response = client.get(
        f"{settings.API_V1_STR}/blog/posts/{item.slug}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["slug"] == unique_slug_generator(test_data["title"])
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
    

def test_read_category(
    client: TestClient,
    superuser_token_headers: dict,
    db: AsyncSession) -> None:
    item = create_random_post(db)
    response = client.get(
        f"{settings.API_V1_STR}/blog/tags/{item.slug}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["slug"] == unique_slug_generator(test_data["title"])
    assert content["id"] == item.id
