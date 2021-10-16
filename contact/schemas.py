from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    """
    Base fields for contact.
    """
    firstname: str
    lastname: str
    email: EmailStr
    message: str

class ContactCreate(ContactBase):
    """
    Fields for creating contacts.
    """
    ...

class ContactOut(ContactBase):
    """
    For Contact response.
    """
    id: Optional[int] = None
    status: bool = True
    created: Optional[datetime] = None
    