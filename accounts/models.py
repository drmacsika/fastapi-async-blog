from typing import TYPE_CHECKING

from core.base import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from blog.models import Post

class User(Base):
    """Account details for authors, editors, and contributors"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    firstname = Column(String(length=100), nullable=False)
    lastname = Column(String(length=100), nullable=False)
    username = Column(String(length=100), nullable=False, unique=True, index=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    active = Column(Boolean, default=False)
    staff = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    articles = relationship("Post", back_populates="author")
    # articles = relationship("Post", cascade="all,delete-orphan", back_populates="author", uselist=True,)
    
    def __repr__(self) -> str:
        return "<User %r %r>" % (self.firstname, self.lastname)
    
    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"
