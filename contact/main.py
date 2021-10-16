from typing import Any, List

from core.settings import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from contact.crud import contact
from contact.schemas import ContactCreate, ContactOut

router = APIRouter()

@router.get("/contacts/", response_model=List[ContactOut])
async def get_all_contacts(
    offset: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to get all contacts."""
    return await contact.get_multiple(db=db, offset=offset, limit=limit)


@router.post("/contact/create/", status_code=201, response_model=ContactOut)
async def create_contact(
    request: ContactCreate,
    db: AsyncSession = Depends(get_session)) -> Any:
    """
    End point for contact creation.
    This should always be placed above the single GET endpoint.
    """
    return await contact.create(obj_in=request, db=db)


@router.get("/contact/{id}")
async def get_contact(
    id: int, 
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to get each contact."""
    return await contact.get(slug=id, db=db)


@router.delete("/contact/{id}/delete/")
async def delete_contact(
    id: int,
    db: AsyncSession = Depends(get_session)) -> Any:
    """Endpoint to delete a contact."""
    return await contact.delete(slug=id, db=db)
