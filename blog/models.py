from core.settings import settings
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = settings.Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(length=100), index=True, nullable=False)
    description = Column(String(length=250), nullable=True)
    intro = Column(String(length=200), nullable=True)
    content = Column(Text)
    post_image = Column(Text)
    slug = Column(String(length=255), nullable=False, unique=True)
    read_length = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    active = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    
    # Relationships
    author = relationship("User", back_populates="articles")
    categories = relationship("Category", back_populates="post")
    
    def __repr__(self) -> str:
        return "<Post %r>" % self.email
    
    def __str__(self) -> str:
        return f"{self.email}"



class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    title = Column(String(length=100), index=True)
    description = Column(String(length=250), nullable=True)
    slug = Column(String(length=255), nullable=False, unique=True)
    active = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="categories")

    def __repr__(self) -> str:
        return "<Category %r>" % self.slug
    
    def __str__(self) -> str:
        return f"{self.slug}"
