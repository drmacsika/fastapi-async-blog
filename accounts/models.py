from core.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = settings.Base

class User(Base):
    """Account details for authors, editors, and contributors"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(), nullable=False)
    lastname = Column(String(), nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    staff = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    
    # Relationships
    articles = relationship("Post", back_populates="author")
    
    # posts = relationship(
    #     "Recipe",
    #     cascade="all,delete-orphan",
    #     back_populates="submitter",
    #     uselist=True,
    # )
