from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///../db.sqlite3"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL =  "postgresql+asyncpg://scott:tiger@postgresserver/db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo = True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Postgres settings
async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session





