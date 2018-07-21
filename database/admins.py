from typing import Union

from discord.abc import Snowflake, User
from peewee import *

from .db import BaseModel


class AdminModel(BaseModel):
    userid = BigIntegerField(primary_key=True)
    permissions = IntegerField(default=1000)

    @classmethod
    def get_or_insert(cls, admin: Union[User, int]):
        if isinstance(admin, Snowflake):
            admin = admin.id
        model, created = cls.get_or_create(userid=admin)
        if created:
            model.save()
        return model
