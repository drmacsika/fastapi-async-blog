from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
SLUGTYPE = TypeVar("SLUGTYPE", "int", "str")

class BaseCRUD(Generic[ModelType, CreateSchema, UpdateSchema, SLUGTYPE]):
    """
    Base class for all crud operations
    Methods to Create, Read, Update, Delete (CRUD).
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(
        self,
        slug: SLUGTYPE,
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
        
    async def create(self, *, obj_in: CreateSchema, db: AsyncSession) -> ModelType:
        """Create an item."""
        obj = jsonable_encoder(obj_in)
        stmt = self.model(**obj)
        db.add(stmt)
        await db.commit()
        await db.refresh(stmt)
        return obj_in
        
    async def update(
        self, *, db_obj: ModelType = None, 
        obj_in: Union[UpdateSchema, Dict[str, Any]], 
        db: AsyncSession,
        slug_field: SLUGTYPE = None
        ) -> ModelType:
        """
        Update an item.
        - *db_obj is an instance of a model class being accessed e.g Post Model.
        - Precisely, the instance calls the get method and we use the 
        - result of that call for the db_obj. This makes all the instance variables
        - invokable to the method and class via the instance.
        - *obj_in is the pydantic validation class. It returns a 
        - key-value pair of all values. Rather than pass each value pair
        - one after the other, we convert to dictionary. Because the original
        - obj_in is simply instance variables with values separated by spaces.
        - By converting to dictionary, we can then unpack to comma-separated 
        - key value pair using **obj_in
        - *jsonable_encoder, takes a list of key-value pair and converts them
        - to dictionary format, 
        - jsonable_encoder(foo) is same as using **foo.dict()
        """
        # if isinstance(obj_in, dict):
        #     updated_data = obj_in
        # else:
        #     updated_data = obj_in.dict(exclude_unset=True)
        # # Loop through the db instance and get the dictionary version of all
        # # instance variables and values gotten from the get method request
        # # The conditional checks to update only the values from the pydantic
        # # Update model that corresponds to the DB model
        # for field in jsonable_encoder(db_obj):
        #     if field in updated_data:
        #         setattr(db_obj, field, updated_data[field])
        # db.add(db_obj)
        # await db.commit()
        # await db.refresh(db_obj)
        obj_in = jsonable_encoder(obj_in)
        stmt = update(self.model).where(self.model.slug == slug_field).values(**obj_in).execution_options(synchronize_session="fetch")
        stmt = await db.execute(stmt)
        await db.commit()
        return db_obj
        
        
        
        
    async def delete(self, *, slug: SLUGTYPE, db: AsyncSession) -> ModelType:
        """Delete an item."""
        stmt = delete(self.model).where(self.model.slug == slug)\
            .execution_options(synchronize_session="fetch")
        await db.execute(stmt)
        await db.commit()
        return {"Detail": "Successfully deleted!"}
        
