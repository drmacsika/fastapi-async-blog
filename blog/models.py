from core.base import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
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



