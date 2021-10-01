from core.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

Base = settings.Base

class Contact(Base):
    """Get contact messages from visitors"""
    
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(255), index=True, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Boolean, default=True)
    created = Column(DateTime, server_default=func.now())
    