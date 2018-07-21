import asyncio
import random

from discord import Member, Embed, Color, Message, Guild, TextChannel
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, Bot

from database import MemberModel

LEVEL_UP_IMAGES = [
    'https://omae-wa-mou.shindei.ru/yQONFEa',
    'https://senpai.will-never-love.me/s9lm8s.png'
]


class Levels(object):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.messaged_in_last_minute = set()
        self.bot.loop.create_task(self.clear_up())

    async def clear_up(self):
        while True:
            await asyncio.sleep(60)
            self.messaged_in_last_minute = set()

    async def on_message(self, msg: Message):
        if msg.guild is None:
            return
        member: Member = msg.author
        if member.bot:
            return
        guild: Guild = msg.guild
        compound = (guild.id, member.id)
        if compound in self.messaged_in_last_minute:
            return
        self.messaged_in_last_minute.add(compound)
        channel: TextChannel = msg.channel
        xp = MemberModel.get_or_insert(msg.author).xp
        MemberModel.update(xp=MemberModel.xp + random.randint(10, 20), admin=member.guild_permissions.administrator) \
            .where((member.id == MemberModel.uid) &
                   (guild.id == MemberModel.gid)).execute()
        new_xp = MemberModel.get_or_insert(msg.author).xp
        if xp // 1000 < new_xp // 1000:
            lvlupmsg = await channel.send(
                embed=Embed(
                    title="LEVEL UP!",
                    description=f"You are now level {new_xp//1000}!",
                    color=Color.green()
                ).set_author(icon_url=member.avatar_url, name=member.display_name))
            await asyncio.sleep(10)
            await lvlupmsg.delete()


    @commands.command()
    @commands.guild_only()
    async def rank(self, ctx: CommandContext, user: Member = None):
        if user is None:
            user: Member = ctx.author
        levels: MemberModel = MemberModel.get_or_insert(user)
        xp: int = levels.xp
        await ctx.send(
            embed=Embed(
                title=f"Level {xp//1000}",
                description=f"{xp} XP Points - {1000 - (xp % 1000)} till level {xp // 1000 + 1}",
                color=Color.blue()
            ).set_author(name=user.display_name, icon_url=user.avatar_url))


def setup(bot: Bot):
    bot.add_cog(Levels(bot))
