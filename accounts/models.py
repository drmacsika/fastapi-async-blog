from core.settings import settings
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

Base = settings.Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    articles = relationship("Post", back_populates="author")
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    staff = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created = Column(DateTime)
    updated = Column(DateTime)
    
    # posts = relationship(
    #     "Recipe",
    #     cascade="all,delete-orphan",
    #     back_populates="submitter",
    #     uselist=True,
    # )
