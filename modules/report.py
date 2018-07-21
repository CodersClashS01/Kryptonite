from discord import TextChannel, Color, Embed, Message, Member, Guild, Reaction, Emoji, PartialEmoji
from discord.ext import commands
from discord.ext.commands import Context as CommandContext
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from discord.raw_models import RawReactionActionEvent
from typing import List
from datetime import datetime

from database import GuildModel


class Reports(object):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def set_report_channel(self, ctx: CommandContext):
        if len(ctx.message.channel_mentions) > 0:
            guild_settings: GuildModel = GuildModel.get_or_insert(ctx.guild)
            guild_settings.report_channel = int(ctx.message.channel_mentions[0].id)
            guild_settings.save()
            await ctx.send(
                embed=Embed(
                    description=f"Changed the report channel to `{ctx.message.channel_mentions[0]}`",
                    color=Color.green()))
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="No channel mention found! You need to mention a channel to set!",
                    color=Color.red()
                )
            )

    @commands.command()
    async def report(self, ctx: CommandContext, to_report: Member, *, reason = ""):
        channel: TextChannel = ctx.channel
        guild_settings: GuildModel = GuildModel.get_or_insert(ctx.guild)
        if not guild_settings.report_channel:
            await channel.send(embed=Embed(color=Color.red(), title="Error", description="There is currently no reports"
                                                                                         " channel set, tell the server"
                                                                                         " admins to set one!"))
            return
        if not to_report:
            await channel.send(embed=Embed(color=Color.red(), title="Error", description="You need to mention a user to#"
                                                                                         " report!"))
        elif reason:
            await channel.send(embed=Embed(color=Color.green(), title="Report Sent", description=f"Reported"
                                                                                                 f" {to_report.mention}"
                                                                                                 f" with reason:\n\n**"
                                                                                                 f"{reason}**"))
            em = Embed(color=Color.green(), title="REPORT", description=f"{to_report.mention} got reported with "
                                                                        f"reason:\n\n**{reason}**")
            em.set_footer(text=f"Reported by {ctx.author} in {ctx.channel} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            msg = await ctx.bot.get_channel(guild_settings.report_channel).send(embed=em)
            await msg.add_reaction('❌')
            await msg.add_reaction('👢')
            await msg.add_reaction('🔨')
        else:
            await channel.send(embed=Embed(color=Color.green(), title="Report Sent", description=f"Reported {to_report.mention} without reason"))
            em = Embed(color=Color.green(), title="REPORT", description=f"{to_report.mention} got reported without reason!")
            em.set_footer(text=f"Reported by {ctx.author} in {ctx.channel} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            msg = await ctx.bot.get_channel(guild_settings.report_channel).send(embed=em)
            await msg.add_reaction('❌')
            await msg.add_reaction('👢')
            await msg.add_reaction('🔨')

    async def on_raw_reaction_add(self, event: RawReactionActionEvent):
        message_id: int = int(event.message_id)
        channel_id: int = int(event.channel_id)
        emoji: PartialEmoji = event.emoji
        if emoji.is_unicode_emoji():
            emoji = str(emoji)
        else:
            emoji = emoji.id
        guild: Guild = self.bot.get_guild(event.guild_id)
        user: Member = guild.get_member(event.user_id)
        message: Message = await guild.get_channel(channel_id).get_message(message_id)
        if message.embeds[0].title == "REPORT":
            pass  # FUCK THIS SHIT AAAAARRGH..... CODING CAN BE SOOOOO ANNOYING ~CCHD
            #  more when you do everthing alone cause nobody has time but nothing works ~BC
            #  Ore when some people say they'll work on something and then start playing games instead ~CCHD
            # *or ~BC

    async def on_command_error(self, ctx: commands.Context, exc: BaseException):
        pass
    #    if isinstance(exc, CommandNotFound):
    #        pass
    #        command: List[str] = ctx.message.content.split(" ")[0]
    #        await ctx.channel.send(embed=Embed(color=Color.red(), title="Error 404", description="Command: **{}**
    # not found!".format(command)))


def setup(bot: commands.Bot):
    bot.add_cog(Reports(bot))
