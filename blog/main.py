from typing import List

from core.settings import get_session, init_models
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.crud import (delete_item, get_item, get_multiple_items, post_item,
                       update_item)
from blog.models import Category, Post
from blog.schemas import (CategoryOut, CreateCategory, CreatePost, PostOut,
                          UpdateCategory, UpdatePost)

router = APIRouter()

@router.post("/blog/create/", status_code=201, response_model = PostOut, tags=["Blog Post"])
async def create_post(request: CreatePost, db: AsyncSession = Depends(get_session)):
    return await post_item(item=request, db=db, cls=Post)

@router.get("/blog/{slug}/", response_model=PostOut, tags=["Blog Post"])
async def get_post(slug: str, db: AsyncSession = Depends(get_session)):
    return get_item(slug=slug, cls=Post, db=db)


@router.get("/blog/", response_model=List[PostOut], tags=["Blog Post"])
async def get_all_posts(db: AsyncSession = Depends(get_session)):
    return await get_multiple_items(cls=Post, db=db)


@router.put("/blog/{slug}/update/", status_code=200, response_model=PostOut, tags=["Blog Post"])
async def update_post(request: UpdatePost, slug: str, db: AsyncSession = Depends(get_session)):
    return await update_item(item=request, slug=slug, db=db, cls=Post)


@router.delete("/blog/{slug}/delete/", status_code=410, response_model=PostOut, tags=["Blog Post"])
async def delete_post(request: UpdatePost, slug: str, db: AsyncSession):
    return await delete_item(item=request, slug=slug, cls=Post, db=db)


@router.post("/blog/tag/create/", status_code=201, response_model=CategoryOut, tags=["Blog Category"])
async def create_category(request: CreateCategory, db: AsyncSession = Depends(get_session)):
    return await post_item(item=request, cls=Category, db=db)


@router.get("/blog/tag/{slug}/", response_model=CategoryOut, tags=["Blog Category"])
async def get_category(slug: str, db: AsyncSession = Depends(get_session)):
    return await get_item(slug=slug, cls=Category, db=db)


@router.get("/blog/tags/", response_model=List[CategoryOut], tags=["Blog Category"])
async def get_all_categories(db: AsyncSession = Depends(get_session)):
    return await get_multiple_items(cls=Category, db=db)


@router.put("/blog/tag/{slug}/update/", status_code=200, response_model=CategoryOut, tags=["Blog Category"])
async def update_category(request: UpdateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    return await update_item(item=request, slug=slug, db=db, cls=Category)
    

@router.delete("/blog/tag/{slug}/delete/", status_code=410, tags=["Blog Category"])
async def delete_category(request: UpdateCategory, slug: str, db: AsyncSession = Depends(get_session), tags=["Blog Category"]):
    return await delete_item(item=request, slug=slug, cls=Category, db=db)
    
