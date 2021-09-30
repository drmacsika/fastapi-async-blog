from core.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

Base = settings.Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Boolean, default=True)
    created = Column(DateTime)
    