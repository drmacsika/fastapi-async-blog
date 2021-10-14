from typing import Optional, Union

from core.crud import BaseCRUD
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from contact.models import Contact
from contact.schemas import ContactCreate

SLUGTYPE = Union[int, str]

class ContactCRUD(BaseCRUD[Contact, ContactCreate, ContactCreate, SLUGTYPE]):
    
    async def create(
        self, *, obj_in: ContactCreate,
        db: AsyncSession, slug_field: SLUGTYPE = None
        ) -> Contact:
        try:
            return await super().create(obj_in, db, slug_field=slug_field)
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def delete(self, *, slug: SLUGTYPE, db: AsyncSession) -> Contact:
        try:
            contact = self.get(slug=slug, db=db)
            if contact:
                return await super().delete(slug=slug, db=db)
            else:
                raise HTTPException(status_code=404, detail="Contact does not exist.")
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se

contact = ContactCRUD(Contact)
