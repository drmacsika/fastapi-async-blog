from core.settings import settings
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

Base = settings.Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    categories = relationship("Category", back_populates="post")
    title = Column(String(length=100), index=True)
    description = Column(String(length=250), nullable=True)
    intro = Column(String(length=200), nullable=True)
    content = Column(Text)
    slug = Column(String)
    read_length = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    active = Column(Boolean, default=False)
    created = Column(DateTime)
    updated = Column(DateTime)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="categories")
    title = Column(String(length=100), index=True)
    description = Column(String(length=250), nullable=True)
    slug = Column(String)
    active = Column(Boolean, default=False)
    created = Column(DateTime)
    updated = Column(DateTime)
