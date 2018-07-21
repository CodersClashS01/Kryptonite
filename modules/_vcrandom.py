import random
from typing import List

from discord import Embed, Color, Member, VoiceState, VoiceChannel
from discord.ext import commands
from discord.ext.commands import Context as CommandContext, Bot


class VCRandomCog(object):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(hidden=True)
    async def random_voice_member(self, ctx: CommandContext):
        if ctx.guild is None:
            return await ctx.send(
                embed=Embed(
                    title="Only available in guilds",
                    color=Color.red()))
        member: Member = ctx.author
        voice: VoiceState = member.voice
        if voice is None:
            return await ctx.send(
                embed=Embed(
                    title="Please join a Voice Channel",
                    color=Color.red()))
        channel: VoiceChannel = voice.channel
        members: List[Member] = channel.members
        if len(members) < 2:
            return await ctx.send(
                embed=Embed(
                    title="YOU LONELY FUCK LOOOOOOOOL",
                    color=Color.red()
                ).set_image(url="http://www.locopengu.com/images/media/750xauto/HG2GT.png"))
        await ctx.send(
            embed=Embed(
                title="Random Voicechat Member",
                description=random.choice(members).mention,
                color=Color.red()))


def setup(bot: Bot):
    bot.add_cog(VCRandomCog(bot))
