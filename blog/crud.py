from typing import Any, Dict, List, Optional, Union

from core.crud import BaseCRUD
from core.dependencies import get_read_length, unique_slug_generator
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
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
        read_length = get_read_length(obj_in.content)
        db_obj = jsonable_encoder(obj_in, exclude=["slug", "read_length"])
        if post:
            slug = unique_slug_generator(obj_in.title, new_slug=True)
        try:
            stmt = Post(**db_obj, slug=slug, read_length=read_length)
            db.add(stmt)
            await db.commit()
            await db.refresh(stmt)
            return db_obj
        except IntegrityError as ie:
            raise ie.orig
        except SQLAlchemyError as se:
            raise se
    
    async def update(
        self, *, db_obj: Post = None, obj_in: Union[UpdatePost, Dict[str, Any]],
        db: AsyncSession, slug_field: SLUGTYPE = None) -> Post:
        """Update blog post"""
        db_obj = await self.get(slug=slug_field, db=db)
        obj_in = jsonable_encoder(obj_in, exclude_unset=True)
        try:
            # if isinstance(obj_in, dict):
            #     updated_data = obj_in
            # else:
            #     updated_data = obj_in.dict(exclude_unset=True)
            # if updated_data["title"]:
            #     new_slug = unique_slug_generator(updated_data["title"])
            #     del updated_data["slug"]
            #     updated_data["slug"] = new_slug           
            return await super().update(db_obj=db_obj, obj_in=obj_in, db=db, slug_field=slug_field)
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
