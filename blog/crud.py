from typing import Any, List

from core.dependencies import (check_existing_row_by_slug, slugify,
                               unique_slug_generator)
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

_errors = {"category": {
    400: "An category with this slug already exists.",
    404: "Requested category does not exist."
},
    "post": {
        400: "A post with this slug already exists.",
        404: "Requested post does not exist."
}
}


async def get_item(*, slug: str, cls: Any, db: AsyncSession) -> Any:
    """
    Get single item based on slug.
    """
    try:
        query = select(cls).where(cls.slug == slug)
        query = await db.execute(query)
        query = query.scalars().first()
        if query is not None:
            return query
        else:
            raise HTTPException(
                status_code=404, detail=_errors[cls.__name__.lower()][404])
    except IntegrityError as ie:
        raise ie.orig
    except SQLAlchemyError as se:
        raise se


async def get_multiple_items(*, cls: Any, db: AsyncSession) -> List[Any]:
    """
    Get all items. 
    ??? May be modified in the future to account for optional query parameters.
    """
    try:
        result = select(cls).order_by(cls.updated)
        result = await db.execute(result)
        return result.scalars().all()
    except IntegrityError as ie:
        raise ie.orig
    except SQLAlchemyError as se:
        raise se


async def post_item(*, item: Any, db: AsyncSession, cls: Any) -> Any:
    """
    Function for posting new item like post or category.
    This checks the row for existing slug based on the title of the item.
    and generates new slug if applicable.
    """
    query = await check_existing_row_by_slug(cls, slugify(item.title), db)
    slug = unique_slug_generator(query, value=item.title, new_slug=True)
    item = jsonable_encoder(item, exclude=["slug"])
    stmt = cls(**item, slug=slug)
    db.add(stmt)
    try:
        await db.commit()
        await db.refresh(stmt)
        return stmt
    except SQLAlchemyError as se:
        await db.rollback()
        raise se
    except ValidationError as e:
        raise e
    except IntegrityError as ie:
        await db.rollback()
        raise ie.orig


async def update_item(*, item: Any, slug: str, db: AsyncSession, cls: Any) -> Any:
    """
    Function performs update method for arbitrary items like category or post.
    - Checks for the existence of the row using the slug.
    - cls.__name__.lower() gets the name lowercase case name of the class
    - **item.dict() unpacks the values from pydantic models rather than pass
    - individual keyword args.
    """
    item = jsonable_encoder(item)
    query = await check_existing_row_by_slug(cls, slug, db, status_code=404, msg=_errors[cls.__name__.lower()][404])
    stmt = update(cls).where(cls.slug == slug).values(
        **item).execution_options(synchronize_session="fetch")
    try:
        stmt = await db.execute(stmt)
        await db.commit()
        return query
    except SQLAlchemyError as se:
        await db.rollback()
        raise se
    except IntegrityError as ie:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Internal Server Error")
    except RequestValidationError:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except ValidationError as e:
        raise e
    finally:
        await db.close()


async def delete_item(*, item: Any, slug: str, cls: Any, db: AsyncSession) -> Any:
    """
    Delete item based on provided slug. Returns status code 410 
    and success message for UX enhancement rather than rather
    """
    await check_existing_row_by_slug(cls, slug, db, status_code=404, msg=_errors[cls.__name__.lower()][404])
    stmt = delete(cls).where(cls.slug == slug).execution_options(
        synchronize_session="fetch")

    try:
        await db.execute(stmt)
        await db.commit()
        return {"Detail": "Successfully deleted!"}
    except IntegrityError as ie:
        await db.rollback()
        raise ie.orig
    except SQLAlchemyError as se:
        await db.rollback()
        raise se
    except RequestValidationError:
        raise HTTPException(status_code=500, detail="Internal Server Error.")
