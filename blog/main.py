from typing import List

from core.settings import get_session, init_models
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from blog.crud import delete_item, get_multiple_items, post_item, update_item
from blog.models import Category
from blog.schemas import CategoryOut, CreateCategory, UpdateCategory

router = APIRouter()


@router.get("/blog/tags", response_model=List[CategoryOut])
async def get_all_categories(db: AsyncSession = Depends(get_session)):
    return await get_multiple_items(db)


@router.post("/blog/tag/create", status_code=201, response_model=CategoryOut)
async def create_category(request: CreateCategory, db: AsyncSession = Depends(get_session)):
    return await post_item(item=request, cls=Category, db=db)


@router.put("/blog/tag/update/{slug}", status_code=200, response_model=CategoryOut)
async def update_category(request: UpdateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    return await update_item(item=request, slug=slug, db=db, cls=Category)
    

@router.delete("/blog/tag/delete/{slug}")
async def delete_category(request: UpdateCategory, slug: str, db: AsyncSession = Depends(get_session)):
    return await delete_item(item=request, slug=slug, cls=Category, db=db)
    # return {"Detail": "Successfully deleted."}
    
