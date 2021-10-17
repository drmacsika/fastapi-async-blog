from accounts.crud import user
from accounts.models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.base import Base
from core.schemas import TokenPayload
from core.settings import settings

# Postgres DB meta settings
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo = True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    # try:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    # finally:
    #     db.close()
    

async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.PASSLIB_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    check_user = await user.get_by_id(id=token_data.sub, db=db)
    if not check_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return check_user


def get_current_active_user(
    current_user: User = Depends(get_current_user),) -> User:
    if not user.is_active(current_user):
        raise HTTPException(status_code=400, detail="This user account is inactive.")
    return current_user


def get_current_active_staff(
    current_user: User = Depends(get_current_user),
) -> User:
    if not user.is_staff(current_user):
        raise HTTPException(
            status_code=400, detail="The user is not a staff."
        )
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user is not an admin."
        )
    return current_user
