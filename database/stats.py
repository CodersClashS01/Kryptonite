from peewee import *

from .db import BaseModel
from typing import Union
from discord.abc import Snowflake


class StatsModel(BaseModel):
    gid = BigIntegerField()
    cidusr = BigIntegerField()
    cidrol = BigIntegerField()


    @classmethod
    def get_or_insert(cls, guild: Union[Snowflake, int]):
        if isinstance(guild, Snowflake):
            guild = guild.id
        model, created = cls.get_or_create(gid=guild)
        if created:
            model.save()
        return model
