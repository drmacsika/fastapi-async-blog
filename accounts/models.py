from core.mixins import AbstractBaseModel, TimestampMixin
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(AbstractBaseModel, TimestampMixin):
    email = fields.CharField(max_length=250, unique=True)
    firstname = fields.CharField(max_length=50, null=False)
    lastname = fields.CharField(max_length=50, null=False)
    token = fields.IntField(default=0)
    active = fields.BooleanField(default=False)
    staff = fields.BooleanField(default=False)
    admin = fields.BooleanField(default=False)
    

    @classmethod
    async def get_user(cls, email):
        return cls.get(email=email)
    
    def verify_token(self, token):
        return True


User_Pydantic = pydantic_model_creator(User, "User")
UserIn_Pydantic = pydantic_model_creator(User, "UserIn", exclude_readonly=True)
UserOut_Pydantic = pydantic_model_creator(User, "userOut", exclude=("token", "id", "active", "created", "updated", "staff", "admin"))
