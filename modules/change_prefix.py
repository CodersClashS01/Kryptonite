from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, Bot

from database import GuildModel


class Settings(object):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def change_prefix(self, ctx: CommandContext, new_prefix):
        guild_settings: GuildModel = GuildModel.get_or_insert(ctx.guild)
        guild_settings.prefix = new_prefix
        guild_settings.save()
        await ctx.send(
            embed=Embed(
                description=f"Changed the prefix to `{new_prefix}`",
                color=Color.green()))


def setup(bot: Bot):
    bot.add_cog(Settings(bot))
