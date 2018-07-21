import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or

from database import GuildModel
from utils import load_all_modules


def get_server_prefix(bot: commands.Bot, message: discord.Message):
    prefixes = ['-']

    if message.guild:
        prefixes = [GuildModel.get_or_insert(message.guild).prefix]

    return when_mentioned_or(*prefixes)(bot, message)


def get_guild(id):
    return client.get_guild(id)


client = Bot(command_prefix=get_server_prefix)


if __name__ == '__main__':
    from config import config

    load_all_modules(client)

    client.run(config.token)
