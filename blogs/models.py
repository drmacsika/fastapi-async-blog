from core.mixins import AbstractBaseModel, BlogMixin, TimestampMixin
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from managers import CategoryManager, PostManager


class Post(AbstractBaseModel, BlogMixin, TimestampMixin):
    excerpt = fields.TextField()
    content = fields.TextField()
    read_length = fields.IntField(default=0)
    view_count = fields.IntField(default=0)
    slug = fields.CharField(max_length=250, unique=True)
    category = fields.ManytoManyField(
        Category, related_name="categories", on_delete='CASCADE')
    
    class Meta:
        table = "posts"
        ordering = ["-created"]
        # manager = PostManager()
    
    def __str__(self):
        return self.title
    


class Category(AbstractBaseModel, BlogMixin, TimestampMixin):
    slug = fields.CharField(max_length=50, unique=True)
    
    class Meta:
        table = "categories"
        ordering = ["title"]
        # manager = CategoryManager()
    
    def __str__(self):
        return self.title

Post_Pydantic = pydantic_model_creator(Post, name="Post", exclude=("active", "view_count", "read_length"))
PostIn_Pydantic = pydantic_model_creator(
    Post, name="PostIn", exclude_readonly=True)
Category_Pydantic = pydantic_model_creator(Category, name="Category", exclude=("active"))
CategoryIn_Pydantic = pydantic_model_creator(
    Category, name="CategoryIn", exclude_readonly=True)
