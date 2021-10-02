from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    SECRET_KEY: str = 'fastapi-secure-&ixxyzs#f+ycdhfwct8d8)b!c*agg3%0n-b_8ywd2rr@eiw-bo'
    # SUPERUSER: EmailStr = "drmacsika@gmail.com"
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite+aiosqlite:///../db.sqlite3"
    # db_user: Optional[str] = ""
    # db_password: Optional[str] = ""
    # SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@postgresserver/db"
    Base = declarative_base()


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

# Postgres DB meta settings
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo = True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(settings.Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        settings.engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
