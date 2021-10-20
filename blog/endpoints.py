from typing import Any, List

from core.dependencies import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete

from blog.crud import category, post
from blog.models import Category, Post
from blog.schemas import (CategoryOut, CreateCategory, CreatePost, PostOut,
                          UpdateCategory, UpdatePost)

router = APIRouter()


@router.get("/blog/", response_model=List[PostOut], tags=["Blog Post"])
async def get_all_posts(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to get all blog posts or filtered blog posts."""
    return await post.get_multiple(db=db, offset=offset, limit=limit)


@router.get("/blog/tags/", response_model=List[CategoryOut], tags=["Blog Category"])
async def get_all_categories(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to get all blog categories or filtered blog categories."""
    return await category.get_multiple(db=db, offset=offset, limit=limit)


@router.post("/blog/", status_code=201, response_model = PostOut, tags=["Blog Post"])
async def create_post(
    request: CreatePost,
    db: AsyncSession = Depends(get_session)) -> Any:
    """
    End point for blog post creation. This should always be placed above
    the blog single GET endpoint.
    """
    return await post.create(obj_in=request, db=db)


@router.post("/blog/tag/", status_code=201, response_model=CategoryOut, tags=["Blog Category"])
async def create_category(
    request: CreateCategory,
    db: AsyncSession = Depends(get_session)) -> Any:
    """
    End point for blog category creation. This should always be placed above
    the blog single GET endpoint.
    """
    return await category.create(obj_in=request, db=db)


@router.get("/blog/{slug}/", response_model=PostOut, tags=["Blog Post"])
async def get_post(slug: str, db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to get single blog post."""
    return await post.get(slug=slug, db=db)


@router.get("/blog/tag/{slug}/", response_model=CategoryOut, tags=["Blog Category"])
async def get_category(slug: str, db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to get single blog category."""
    return await category.get(slug=slug, db=db)


@router.put("/blog/{slug}/", status_code=200, response_model=PostOut, tags=["Blog Post"])
async def update_post(
    request: UpdatePost,
    slug: str, db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to update blog post."""
    return await post.update(obj_in=request, db=db, slug_field=slug)


@router.put("/blog/tag/{slug}/", status_code=200, response_model=CategoryOut, tags=["Blog Category"])
async def update_category(
    request: UpdateCategory, 
    slug: str, 
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to update blog category."""
    return await category.update(db_obj=Category, obj_in=request, db=db, slug_field=slug)


@router.delete("/blog/{slug}/", tags=["Blog Post"])
async def delete_post(
    slug: str,
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to delete blog post."""
    return await post.delete(slug=slug, db=db)
    

@router.delete("/blog/tag/{slug}/", tags=["Blog Category"])
async def delete_category(
    slug: str,
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to delete blog category."""
    return await category.delete(slug=slug, db=db)
    
