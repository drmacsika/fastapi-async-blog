# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker

# from core.settings import settings

# engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo = True)
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# # Postgres settings
# async def init_models():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(settings.Base.metadata.create_all)


# async def get_session() -> AsyncSession:
#     async_session = sessionmaker(
#         engine, class_=AsyncSession, expire_on_commit=False
#     )
#     async with async_session() as session:
#         yield session


