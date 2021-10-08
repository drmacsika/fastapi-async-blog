"""
imports for Base and all app models 
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from accounts.models import User
from blog.models import Category, Post
from contact.models import Contact
