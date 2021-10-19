from datetime import timedelta
from typing import Any, Dict, Optional, Union

from core.crud import BaseCRUD
from core.settings import settings
from core.utils import (create_access_token, get_password_hash,
                        send_new_account_email, verify_password)
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.models import User
from accounts.schemas import UserCreate, UserUpdate

SLUGTYPE = Union[str, int]

class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate, SLUGTYPE]):
    """CRUD Function for getting User Accounts."""
    
    async def get(self, *, email: EmailStr, db: AsyncSession) -> Optional[User]:
        """
        Get single user by provided email address.
        We make a new query because the slug is the email and not a default
        slug field as in the super() class.
        """
        query = select(User).where(User.email == email)
        query = await db.execute(query)
        return query.scalars().first()
    
    async def get_by_id(self, id: int, db: AsyncSession) -> Optional[User]:
        """Get a single user by id"""
        query = select(User).where(User.id == id)
        query = await db.execute(query)
        return query.scalars().first()
    
    async def create(self, *, obj_in: UserCreate, db: AsyncSession, slug_field: str = None) -> User:
        try:
            user = await self.get(email=obj_in.email, db=db)
            if not user:
                user = User(
                    jsonable_encoder(**obj_in),
                    password=get_password_hash(obj_in.password)
                )
                db.add(user)
                await db.commit()
                if settings.EMAILS_ENABLED and obj_in.email:
                    send_new_account_email(
                        email_to=obj_in.email,
                        username=obj_in.email, 
                        password=obj_in.password
                )
                await db.refresh(user)
                return user
            else:
                raise HTTPException(status_code=404, detail="User already exist.")
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def update(
        self, *,
        obj_in: Union[UserUpdate, Dict[str, Any]], 
        db: AsyncSession,
        slug_field: str = None
    ) -> User:
        try:
            user = await self.get(email=slug_field)    
            if not user:
                raise HTTPException(status_code=404, detail="User does not exist.")
            if not isinstance(obj_in, dict):
                obj_in = jsonable_encoder(obj_in, exclude_unset=True)
            if obj_in["password"]:
                hashed_password = get_password_hash(obj_in["password"])
                obj_in.update({"password": hashed_password})
            return await super().update(db=db, db_obj=user, obj_in=obj_in)
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
        
    async def authenticate(
        self, *, email: str, password: str,
        db: AsyncSession) -> Optional[User]:
        """generate and access token to Authenticate a user"""
        
        user = await self.get(email=email, db=db)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=404, detail="Incorrect email or password.")
        elif not self.is_active(user):
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
        

    def is_active(self, user: User) -> bool:
        return user.active
    
    def is_staff(self, user: User) -> bool:
        return user.staff

    def is_superuser(self, user: User) -> bool:
        return user.admin


user = UserCRUD(User)
