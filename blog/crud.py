from typing import Any
from unicodedata import category

from core.dependencies import slugify
from fastapi import HTTPException, status
from sqlalchemy import insert, schema, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.models import Category, Post
from blog.schemas import CreateCategory, UpdateCategory


async def get_categories(db: AsyncSession) -> list[Category]:
    """
    Get all categories.
    """
    try:
        result = select(Category).order_by(Category.updated)
        result = await db.execute(result)
        return result.scalars().all()    
    except IntegrityError as ie:
        raise (ie.orig)
    except SQLAlchemyError as se:
        raise se


async def post_category(category: CreateCategory, slug: str, db: AsyncSession) -> Any:
    """
    Create a new category if it does not already exist.
    Use the slug field for unique constraints.
    """
    try:
        tag = select(Category).where(Category.slug == slug)
        tag = await db.execute(tag)
        tag = tag.scalar()
        if tag is None:
            tag = Category(title=category.title, description=category.description, slug=slugify(category.title))
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
            return tag
        else:
            raise HTTPException(status_code=400, detail = "A category with this slug already exists.")
    except IntegrityError as ie:
        raise (ie.orig)
    except SQLAlchemyError as se:
        raise se

async def put_category(category: UpdateCategory, slug: str, db:AsyncSession):
    try:
        query = select(Category).where(Category.slug == slug)
        query = await db.execute(query)
        query = query.scalar()
        if query:
            query = update(Category).where(Category.slug == slug).values(category).execution_options(synchronize_session="fetch")
            await db.execute(query)
            await db.commit()
            return query
        else:
            raise HTTPException(status_code=404, detail = "This post does not exists.")
    except IntegrityError as ie:
        raise (ie.orig)
    except SQLAlchemyError as se:
        raise se
        

    








# from sqlalchemy import update as sqlalchemy_update
# class ModelAdmin:
#     @classmethod
#     async def create(cls, **kwargs):
#         async_db_session.add(cls(**kwargs))
#         await async_db_session.commit()
#     @classmethod
#     async def update(cls, id, **kwargs):
#         query = (
#             sqlalchemy_update(User)
#             .where(User.id == id)
#             .values(**kwargs)
#             .execution_options(synchronize_session="fetch")
#         )
#         await async_db_session.execute(query)
#         await async_db_session.commit()
#     @classmethod
#     async def get(cls, id):
#         query = select(cls).where(cls.id == id)
#         results = await async_db_session.execute(query)
#         (result,) = results.one()
#         return result



# class ModelAdmin:
#     @classmethod
#     async def create(cls, **kwargs):
#         async_db_session.add(cls(**kwargs))
#         await async_db_session.commit()

#     @classmethod
#     async def update(cls, id, **kwargs):
#         query = (
#             sqlalchemy_update(cls)
#             .where(cls.id == id)
#             .values(**kwargs)
#             .execution_options(synchronize_session="fetch")
#         )

#         await async_db_session.execute(query)
#         await async_db_session.commit()
































