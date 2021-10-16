from typing import Any, Dict, Optional, Union

from core.crud import BaseCRUD
from core.security import get_password_hash, verify_password
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoders
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from accounts.models import User
from accounts.schemas import UserCreate, UserUpdate


class UserCRUD(BaseCRUD[User, UserCreate, UserUpdate]):
    """CRUD Function for getting User Accounts."""
    
    async def get(self, *, email: EmailStr, db: AsyncSession) -> Optional[User]:
        """Get single user by provided email address."""
        query = select(User).where(User.email == email)
        query = await db.execute(query)
        return query.scalars().first()
    
    async def create(self, *, obj_in: UserCreate, db: AsyncSession, slug_field: str = None) -> User:
        try:
            user = await self.get(email=slug_field, db=db)
            if not user:
                user = User(
                    jsonable_encoders(**obj_in),
                    password=get_password_hash(obj_in.password)
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return user
            else:
                raise HTTPException(status_code=404, detail="User already exist.")
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
        
    
    async def update(self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]], db: AsyncSession, slug_field: str = None) -> User:
        try:
            user = await self.get(email=slug_field)
            if user:
                if isinstance(obj_in, dict):
                    updated_data = obj_in
                else:
                    updated_data = obj_in.dict(exclude_unset=True)
                if updated_data["password"]:
                    hashed_password = get_password_hash(updated_data["password"])
                    del updated_data["password"]
                    updated_data["password"] = hashed_password
                return await super().update(db, db_obj=db_obj, obj_in=updated_data)
            else:
                raise HTTPException(status_code=404, detail="User does not exist.")
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
        
    async def authenticate(self, *, email: str, password: str, db: AsyncSession) -> Optional[User]:
        user = await self.get(email=email, db=db)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=404, detail="Incorrect email or password.")
        return user

    def is_active(self, user: User) -> bool:
        return user.active
    
    def is_staff(self, user: User) -> bool:
        return user.staff

    def is_superuser(self, user: User) -> bool:
        return user.admin


crud = UserCRUD(User)