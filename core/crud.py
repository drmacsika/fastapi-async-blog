from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoders
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)

class BaseCRUD(Generic[ModelType, CreateSchema, UpdateSchema]):
    """
    Base class for all crud operations
    Methods to Create, Read, Update, Delete (CRUD).
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(
        self,
        slug: str,
        db: AsyncSession) -> Optional[ModelType]:
        """Get single item."""
        query = select(self.model).where(self.model.slug == slug)
        query = await db.execute(query)
        return query.scalars().first()
    
    async def get_multiple(
        self, *, db: AsyncSession, offset: int = 0,
        limit: int = 0) -> List[ModelType]:
        """get multiple items using a query limiting flag."""
        query = select(self.model).order_by(self.model.created)\
            .offset(offset).limit(limit)
        query = await db.execute(query)
        return query.scalars().all()
        
    async def create(self, *, obj_in: CreateSchema, db: AsyncSession, 
                    slug_field: str = None) -> ModelType:
        """Create an item."""
        stmt = self.model(jsonable_encoders(**obj_in))
        db.add(stmt)
        await db.commit()
        await db.refresh(stmt)
        return stmt
        
    async def update(
        self, *, db_obj: ModelType, 
        obj_in: Union[UpdateSchema, Dict[str, Any]], 
        db: AsyncSession,
        slug_field: str = None
        ) -> ModelType:
        """Update an item."""
        if isinstance(obj_in, dict):
            updated_data = obj_in
        else:
            updated_data = obj_in.dict(exclude_unset=True)
        for field in jsonable_encoders(db_obj):
            if field in updated_data:
                setattr(db_obj, field, updated_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
        
    async def delete(self, *, slug: str, db: AsyncSession) -> ModelType:
        """Delete an item."""
        stmt = delete(self.model).where(self.model.slug == slug)\
            .executable_options(synchronize_session="fetch")
        await db.execute(stmt)
        await db.commit()
        return {"Detail": "Successfully deleted!"}
        
