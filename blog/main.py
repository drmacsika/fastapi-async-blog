from typing import List

from core.settings import get_session, init_models
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.crud import get_categories, post_category
from blog.schemas import Category, CreateCategory

router = APIRouter()


@router.get("/blog/tags", response_model=List[Category])
async def blog(db: AsyncSession = Depends(get_session)):
    categories = await get_categories(db)
    return categories

@router.post("/blog/tag/create", response_model=Category)
async def create_category(request: CreateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    return await post_category(request, slug, db)



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
