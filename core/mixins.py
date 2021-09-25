from tortoise import fields
from tortoise.models import Model


class TimestampMixin():
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

class BlogMixin():
    title = fields.CharField(max_length=250)
    description = fields.TextField(null=True, blank=True)
    active = fields.BooleanField(default=False)

class AbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True

