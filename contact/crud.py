from typing import List, Optional, Union

from core.crud import BaseCRUD
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete

from contact.models import Contact
from contact.schemas import ContactCreate

SLUGTYPE = Union[str, int]

class ContactCRUD(BaseCRUD[Contact, ContactCreate, ContactCreate, SLUGTYPE]):
    
    async def get(
        self, *,
        slug: SLUGTYPE,
        db: AsyncSession) -> Optional[Contact]:
        """Get single item."""
        try:
            contact = select(Contact).where(Contact.id == slug)
            contact = await db.execute(contact)
            contact = contact.scalars().first()
            if not contact:
                raise HTTPException(status_code=404, detail="Contact not found.")
            return contact
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
        
    async def get_multiple(
        self, *,
        db: AsyncSession,
        offset: int = 0, 
        limit: int = 100) -> List[Contact]:
        try:
            contacts = await super().get_multiple(db=db, offset=offset, limit=limit)
            if not contacts:
                raise HTTPException(status_code=404, detail="Contacts not found.")
            return contacts
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def create(self, *, obj_in: ContactCreate, db: AsyncSession) -> Contact:
        try:
            return await super().create(obj_in=obj_in, db=db)
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def delete(self, *, slug: SLUGTYPE, db: AsyncSession) -> Contact:
        try:
            await self.get(slug=slug, db=db)
            stmt = delete(Contact).where(Contact.id == slug)\
                .execution_options(synchronize_session="fetch")
            await db.execute(stmt)
            await db.commit()
            return {"detail": "Deleted successfully!"}            
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se

contact = ContactCRUD(Contact)
