from core.base import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func


class Contact(Base):
    """Get contact messages from visitors"""
    
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Boolean, default=True)
    created = Column(DateTime, server_default=func.now())
    
    def __repr__(self) -> str:
        return "<Contact %r>" % self.email
    
    def __str__(self) -> str:
        return f"{self.email}"
