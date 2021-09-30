from core.mixins import AbstractBaseModel, TimestampMixin
from core.settings import settings
from sikademacsika.backend.src.core.settings import Settings
from sqlachemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

Base = settings.Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    articles = relationship("Post", back_populates="author")
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    staff = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    
    # posts = relationship(
    #     "Recipe",
    #     cascade="all,delete-orphan",
    #     back_populates="submitter",
    #     uselist=True,
    # )
