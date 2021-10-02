from core.settings import settings

Base = settings.Base


from accounts.models import User
from blog.models import Category, Post
from contact.models import Contact
