from core.mixins import AbstractBaseModel, TimestampMixin
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(AbstractBaseModel, TimestampMixin):
    email = fields.CharField(max_length=250, unique=True)
    firstname = fields.CharField(max_length=50, null=False)
    lastname = fields.CharField(max_length=50, null=False)
    token = fields.CharField(max_length=6, default=0)
    active = fields.BooleanField(default=False)
    staff = fields.BooleanField(default=False)
    admin = fields.BooleanField(default=False)
    

    @classmethod
    async def get_user(cls, email):
        return cls.get(email=email)
    
    def full_name(self) -> str:
        if self.firstname or self.lastname:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.email

    class PydanticMeta:
        computed = ["full_name"]
        # exclude = ["password_hash"]
        
    # def verify_otp(self, token):
    #     return hotp.verify('316439', 1401) # => True


User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserOut_Pydantic = pydantic_model_creator(User, name="userOut", exclude=("token", "id", "active", "created", "updated", "staff", "admin"))
