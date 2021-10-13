from typing import List

from core.settings import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from blog.crud import (delete_item, get_item, get_multiple_items, post_item,
                       update_item)
from blog.models import Category, Post
from blog.schemas import (CategoryOut, CreateCategory, CreatePost, PostOut,
                          UpdateCategory, UpdatePost)

router = APIRouter()


@router.get("/blog/", response_model=List[PostOut], tags=["Blog Post"])
async def get_all_posts(db: AsyncSession = Depends(get_session)):
    """Endpoint to get all blog posts or filtered blog posts."""
    return await get_multiple_items(cls=Post, db=db)


@router.get("/blog/tags/", response_model=List[CategoryOut], tags=["Blog Category"])
async def get_all_categories(db: AsyncSession = Depends(get_session)):
    """Endpoint to get all blog posts or filtered blog posts."""
    return await get_multiple_items(cls=Category, db=db)



@router.post("/blog/create/", status_code=201, response_model = PostOut, tags=["Blog Post"])
async def create_post(request: CreatePost, db: AsyncSession = Depends(get_session)):
    """
    End point for blog post creation. This should always be placed above
    the blog single GET endpoint.
    """
    return await post_item(item=request, db=db, cls=Post)


@router.post("/blog/tag/create/", status_code=201, response_model=CategoryOut, tags=["Blog Category"])
async def create_category(request: CreateCategory, db: AsyncSession = Depends(get_session)):
    """
    End point for blog category creation. This should always be placed above
    the blog single GET endpoint.
    """
    return await post_item(item=request, cls=Category, db=db)


@router.get("/blog/{slug}/", response_model=PostOut, tags=["Blog Post"])
async def get_post(slug: str, db: AsyncSession = Depends(get_session)):
    """Endpoint to get single blog post."""
    return await get_item(slug=slug, cls=Post, db=db)


@router.get("/blog/tag/{slug}/", response_model=CategoryOut, tags=["Blog Category"])
async def get_category(slug: str, db: AsyncSession = Depends(get_session)):
    """Endpoint to get single blog category."""
    return await get_item(slug=slug, cls=Category, db=db)


@router.put("/blog/{slug}/update/", status_code=200, response_model=PostOut, tags=["Blog Post"])
async def update_post(request: UpdatePost, slug: str, db: AsyncSession = Depends(get_session)):
    """Endpoint to update blog post."""
    return await update_item(item=request, slug=slug, db=db, cls=Post)


@router.put("/blog/tag/{slug}/update/", status_code=200, response_model=CategoryOut, tags=["Blog Category"])
async def update_category(request: UpdateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    """Endpoint to update blog category."""
    return await update_item(item=request, slug=slug, db=db, cls=Category)


@router.delete("/blog/{slug}/delete/", status_code=410, response_model=PostOut, tags=["Blog Post"])
async def delete_post(request: UpdatePost, slug: str, db: AsyncSession = Depends(get_session)):
    """Endpoint to delete blog post."""
    return await delete_item(item=request, slug=slug, cls=Post, db=db)
    

@router.delete("/blog/tag/{slug}/delete/", status_code=410, tags=["Blog Category"])
async def delete_category(request: UpdateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    """Endpoint to delete blog category."""
    return await delete_item(item=request, slug=slug, cls=Category, db=db)
    
