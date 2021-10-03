from sqlalchemy import schema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.models import Category, Post
from blog.schemas import *


def create_category(category: CreateCategory, db: AsyncSession):
    tag = db.query(Category).filter(Category.slug == category.)
    














# async def create_category(category: schemas.CreateCategory, db: AsyncSession):
#     try:
#         tag = await db.query(models.Category).filter(models.Category.slug == category.slug).first()
#         if(tag is None):
#             category = models.Category(**category.dict())
#             db.add(category)
#             await db.commit()
#             await db.refresh(category)
#             return category
#         else:
#             return f"Category with the slug \"{category.slug}\""
#     except:
#         ...































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
