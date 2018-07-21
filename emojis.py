"""
A little library for loading globally used emojis in the bot.

"""

from typing import List

from discord import Emoji, Guild
from discord.ext.commands import Bot

from config import config


class WrongEmoteException(Exception):
    """
    Exception risen when an :class:`discord.Emote` is found with a wrong name
    """


class MissingEmoteException(Exception):
    """
    Exception risen when an Emote is missing in an :class:`EmoteArsenal`
    """


class EmoteArsenal(object):
    """
    Contains a full arsenal of emojis used globally by the bot

    """
    horse: Emoji
    money: Emoji

    def verify(self):
        """
        verifies this emote arsenal to contain all required emojis

        :raises MissingEmoteException: if an emote is missing
        :raises WrongEmtoeException: if a wrongly named emote is found
        :return: this arsenal
        """
        try:
            if self.horse.name != 'horse':
                raise WrongEmoteException
            if self.money.name != 'money':
                raise WrongEmoteException
        except AttributeError:
            raise MissingEmoteException
        return self


def get_arsenal(bot: Bot, support_guild: int = config.support_guild, no_verify: bool = False) -> EmoteArsenal:
    """
    Gets all emotes the bot will use globally in a handy object

    :param bot: the bot that will be used to find emojis in the support guild
    :param support_guild: the guild id where we will search for emojis
    :raises MissingEmoteException: If an emote is missing in the support guild
    :return: a full emote arsenal
    """
    guild: Guild = bot.get_guild(support_guild)
    if guild is None:
        raise MissingEmoteException
    emojis: List[Emoji] = guild.emojis
    arsenal = EmoteArsenal()
    for emoji in emojis:
        if emoji.name == 'horse':
            arsenal.horse = emoji
        elif emoji.name == 'money':
            arsenal.money = emoji
    if not no_verify:
        arsenal.verify()
    return arsenal
