from typing import Union

from discord.abc import Snowflake
from peewee import *

from .db import BaseModel


class GuildModel(BaseModel):
    gid = BigIntegerField(primary_key=True)
    prefix = CharField(default='-', max_length=5)
    report_channel = BigIntegerField(null=True)
    modlog_channel = BigIntegerField(null=True)

    @classmethod
    def get_or_insert(cls, guild: Union[Snowflake, int]):
        if isinstance(guild, Snowflake):
            guild = guild.id
        model, created = cls.get_or_create(gid=guild)
        if created:
            model.save()
        return model
