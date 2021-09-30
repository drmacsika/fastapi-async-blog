from datetime import datetime

from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    message: str

class ContactCreate(ContactBase):
    ...

class Contact(ContactBase):
    id: int
    status: bool = True
    created: datetime
    