import re
from typing import Any, Dict, List, Optional, Union

from core.crud import BaseCRUD
from core.utils import get_read_time, unique_slug_generator
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from blog.models import Category, Post
from blog.schemas import CreateCategory, CreatePost, UpdateCategory, UpdatePost

SLUGTYPE = Union[int, str]

class PostCrud(BaseCRUD[Post, CreatePost, UpdatePost, SLUGTYPE]):
    """CRUD class for Blog Posts"""
    
    async def get(self, slug: SLUGTYPE, db: AsyncSession) -> Optional[Post]:
        """Get a single blog post"""
        try:
            post = await super().get(slug=slug, db=db)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found.")
            return post
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def get_multiple(self, *, db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Post]:
        """Get multiple blog posts."""
        try:
            posts = await super().get_multiple(db=db, offset=offset, limit=limit)
            if not posts:
                raise HTTPException(status_code=404, detail="No post available.")
            return posts
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def create(self, *, obj_in: CreatePost, db: AsyncSession) -> Post:
        """Create a new blog post with an author an category"""
        slug = unique_slug_generator(obj_in.title)
        post = await super().get(slug=slug, db=db)
        read_time = get_read_time(obj_in.content)
        db_obj = jsonable_encoder(obj_in, exclude=["slug", "read_time"])
        if post:
            slug = unique_slug_generator(obj_in.title, new_slug=True)
        try:
            stmt = Post(**db_obj, slug=slug, read_time=read_time)
            db.add(stmt)
            await db.commit()
            await db.refresh(stmt)
            return db_obj
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def update(
        self, *, obj_in: Union[UpdatePost, Dict[str, Any]],
        db: AsyncSession, slug_field: SLUGTYPE = None) -> Post:
        """Update blog post"""
        post = await self.get(slug=slug_field, db=db)
        try:
            if not isinstance(obj_in, dict):
                obj_in = jsonable_encoder(obj_in, exclude_unset=True)
                
            if obj_in["read_time"] is not None:
                obj_in.update({"read_time": get_read_time(obj_in["content"])})
                
            stmt = update(Post).where(Post.slug == slug_field).values(
                **obj_in, slug=slug_field).execution_options(synchronize_session="fetch")
            stmt = await db.execute(stmt)
            await db.commit()
            return post        
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def delete(self, *, slug: SLUGTYPE, db: AsyncSession) -> Post:
        """Delete a blog post."""
        try:
            await self.get(slug=slug, db=db)
            return await super().delete(slug=slug, db=db)
        except IntegrityError as ie:
            raise ie.orig
        except ValidationError as ve:
            raise ve
        except SQLAlchemyError as se:
            raise se
            


class CategoryCrud(BaseCRUD[Post, CreateCategory, UpdateCategory, SLUGTYPE]):
    """CRUD class for Blog Categories or tags"""
    
    async def get(self, slug: SLUGTYPE, db: AsyncSession) -> Optional[Category]:
        """Get a single blog category."""
        try:
            category = await super().get(slug=slug, db=db)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found.")
            return category
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def get_multiple(self, *, db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Category]:
        """Get multiple blog categories."""
        try:
            categories = await super().get_multiple(db=db, offset=offset, limit=limit)
            if not categories:
                raise HTTPException(status_code=404, detail="No category available.")
            return categories
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def create(self, *, obj_in: CreateCategory, db: AsyncSession) -> Category:
        """Create a new blog category."""
        slug = unique_slug_generator(obj_in.title)
        category = await super().get(slug=slug, db=db)
        db_obj = jsonable_encoder(obj_in, exclude=["slug"])
        if category:
            slug = unique_slug_generator(obj_in.title, new_slug=True)
        try:
            stmt = Category(**db_obj, slug=slug)
            db.add(stmt)
            await db.commit()
            await db.refresh(stmt)
            return stmt
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def update(
        self, *, db_obj: Category = None, obj_in: Union[UpdateCategory, Dict[str, Any]],
        db: AsyncSession, slug_field: SLUGTYPE = None) -> Category:
        """Update blog category"""
        db_obj = await self.get(slug=slug_field, db=db)
        obj_in = jsonable_encoder(obj_in, exclude_unset=True)
        try:       
            return await super().update(db_obj=db_obj, obj_in=obj_in, db=db, slug_field=slug_field)
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def delete(self, *, slug: SLUGTYPE, db: AsyncSession) -> Category:
        """Delete a blog category."""
        try:
            await self.get(slug=slug, db=db)
            return await super().delete(slug=slug, db=db)
        except IntegrityError as ie:
            raise ie.orig
        except ValidationError as ve:
            raise ve
        except SQLAlchemyError as se:
            raise se
            

post = PostCrud(Post)
category = CategoryCrud(Category)
