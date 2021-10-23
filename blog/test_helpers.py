from typing import Optional

from accounts.test_helpers import create_random_user
from core.test_utils import random_lower_string
from sqlalchemy.ext.asyncio import AsyncSession

from blog.crud import category, post
from blog.models import Category, Post
from blog.schemas import CreateCategory, CreatePost


def create_random_post(
    db: AsyncSession, *,
    author_id: Optional[int] = None) -> Post:
    if author_id is None:
        user = create_random_user(db)
        author_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    obj_in = CreatePost(title=title, description=description, author_id=author_id)
    return post.create(db=db, obj_in=obj_in)


def create_random_category(db: AsyncSession) -> Category:
    title = random_lower_string()
    description = random_lower_string()
    obj_in = CreateCategory(title=title, description=description, id=id)
    return category.create(db=db, obj_in=obj_in)
