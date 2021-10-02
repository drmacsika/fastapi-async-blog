from datetime import datetime

from pydantic import BaseModel, EmailStr

"""Base fields for contact."""
class ContactBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    message: str

"""Fields for creating contacts."""
class ContactCreate(ContactBase):
    ...

"""For the response."""
class Contact(ContactBase):
    id: int
    status: bool = True
    created: datetime
    