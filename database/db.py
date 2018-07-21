from peewee import *

from config import config

config = config.mysql
database = MySQLDatabase(config.database, host=config.host, user=config.user, password=config.password)


class BaseModel(Model):
    class Meta:
        database = database
