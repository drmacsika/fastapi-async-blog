from typing import Any
from unicodedata import category

from core.dependencies import slugify
from fastapi import HTTPException, status
from sqlalchemy import insert, schema, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.models import Category, Post
from blog.schemas import CreateCategory


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
            raise HTTPException(status_code=400, detail = "This slug or title already exists.")
    except IntegrityError as ie:
        raise (ie.orig)
    except SQLAlchemyError as se:
        raise se

# async update categories(category)










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

#     @classmethod
#     async def get(cls, id):
#         query = select(cls).where(cls.id == id)
#         results = await async_db_session.execute(query)
#         (result,) = results.one()
#         return result
































# from fastapi import Depends, FastAPI
# from sqlalchemy import select
# from sqlmodel import Session

# from app.db import get_session, init_db
# from app.models import Song, SongCreate

# app = FastAPI()


# @app.get("/ping")
# async def pong():
#     return {"ping": "pong!"}


# @app.get("/blog/", response_model=list[Song])
# def get_songs(session: Session = Depends(get_session)):
#     result = session.execute(select(Song))
#     songs = result.scalars().all()
#     return [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]


# @app.post("/songs")
# def add_song(song: SongCreate, session: Session = Depends(get_session)):
#     song = Song(name=song.name, artist=song.artist)
#     session.add(song)
#     session.commit()
#     session.refresh(song)
#     return song



# from fastapi import Depends, FastAPI
# from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.db import get_session, init_db
# from app.models import Song, SongCreate

# app = FastAPI()


# @app.on_event("startup")
# async def on_startup():
#     await init_db()


# @app.get("/ping")
# async def pong():
#     return {"ping": "pong!"}


# @app.get("/songs", response_model=list[Song])
# async def get_songs(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(Song))
#     songs = result.scalars().all()
#     return [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]


# @app.post("/songs")
# async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
#     song = Song(name=song.name, artist=song.artist)
#     session.add(song)
#     await session.commit()
#     await session.refresh(song)
#     return song
