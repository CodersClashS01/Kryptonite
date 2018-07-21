from discord import Member
from peewee import *

from .db import BaseModel


class MemberModel(BaseModel):
    gid = BigIntegerField()
    uid = BigIntegerField()
    xp = BigIntegerField(default=0)
    admin = BooleanField()

    class Meta:
        primary_key = CompositeKey('gid', 'uid')

    @classmethod
    def get_or_insert(cls, user: Member):
        model, created = cls.get_or_create(gid=user.guild.id, uid=user.id, defaults={
            'admin': user.guild_permissions.administrator,
        })
        if created:
            model.save()
        return model
