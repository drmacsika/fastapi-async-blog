from typing import List

from core.settings import get_session, init_models
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.crud import get_categories, post_category
from blog.schemas import Category, CreateCategory

router = APIRouter()


@router.get("/blog/tags", response_model=List[Category])
async def blog(db: AsyncSession = Depends(get_session)):
    categories = await get_categories(db)
    return categories

@router.post("/blog/tag/create", status_code=201, response_model=Category)
async def create_category(request: CreateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    return await post_category(request, slug, db)

