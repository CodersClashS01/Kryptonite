from datetime import datetime, timedelta

from discord import TextChannel, Color, Embed, Message, Game
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, has_permissions

from config import config
from database import StatsModel


class Info(object):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name=config.game))

        print('#' * 50)
        print(f'Id:     {self.bot.user.id:d}')
        print(f'Name:   {self.bot.user.name}#{self.bot.user.discriminator}')
        print(f"Guilds: {', '.join(guild.name for guild in self.bot.guilds)}")
        print('#' * 50)

    async def on_member_join(self, member):
        try:
            stats: StatsModel = StatsModel.get_or_insert(member.guild)
            if stats.cidusr is not None:
                chan = self.bot.get_channel(stats.cidusr)
                await chan.edit(name="Member: " + str(len(member.guild.members)))
        except Exception as e:
            print(e)
            pass

    async def on_member_remove(self, member):
        try:
            stats: StatsModel = StatsModel.get_or_insert(member.guild)
            if stats.cidusr is not None:
                chan = self.bot.get_channel(stats.cidusr)
                await chan.edit(name="Member: " + str(len(member.guild.members)))
        except Exception as e:
            print(e)
            pass

    async def on_guild_role_create(self, role):
        try:
            stats: StatsModel = StatsModel.get_or_insert(role.guild)
            if stats.cidrol is not None:
                chan = self.bot.get_channel(stats.cidrol)
                await chan.edit(name="Roles: " + str(len(role.guild.roles)))
        except Exception as e:
            print(e)
            pass

    async def on_guild_role_delete(self, role):
        try:
            stats: StatsModel = StatsModel.get_or_insert(role.guild)
            if stats.cidrol is not None:
                chan = self.bot.get_channel(stats.cidrol)
                await chan.edit(name="Roles: " + str(len(role.guild.roles)))
        except Exception as e:
            print(e)
            pass


    @commands.command()
    async def ping(self, ctx: CommandContext):
        channel: TextChannel = ctx.channel
        message: Message = ctx.message
        now = datetime.utcnow()
        ping: timedelta = now - message.created_at
        ping = ping.microseconds / 1000
        await channel.send(
            embed=Embed(
                color=Color.magenta(),
                description='My Ping is `{:.2f}ms`'.format(ping)))

    @commands.command()
    @has_permissions(manage_guild=True)
    async def channel_serverinfo(self, ctx: CommandContext):
        cat = await ctx.guild.create_category_channel("SERVER STATS")
        memb = await ctx.guild.create_voice_channel(category=cat, name="Member: " + str(len(ctx.guild.members)))
        memb3 = await ctx.guild.create_voice_channel(category=cat, name="Roles: " + str(len(ctx.guild.roles)))
        memb2 = await ctx.guild.create_voice_channel(category=cat, name="Owner: " + str(ctx.guild.owner.name))
        stats: StatsModel = StatsModel.get_or_insert(ctx.guild)
        stats.cidusr = int(memb.id)
        stats.cidrol = int(memb3.id)
        stats.save()


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
