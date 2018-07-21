import asyncio

from discord import Embed, Color, Message, Member, Reaction
from discord.ext.commands import Bot, Context as CommandContext, command, group, Group, has_permissions

YES_REACTION = "\U00002705"
NO_REACTION = "\U0000274c"


async def create_action_poll(ctx: CommandContext, description, callback):
    message: Message = await ctx.send(
        embed=Embed(
            description=description,
            color=Color.blurple(),
        )
            .set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            .set_footer(text="This poll will be closed in 30 minutes"))
    await message.add_reaction(YES_REACTION)
    await message.add_reaction(NO_REACTION)
    # await asyncio.sleep(30)# das sind nur 30 sec @roman
    await asyncio.sleep(1800)
    message: Message = await ctx.get_message(message.id)
    yes = None
    no = None
    for reaction in message.reactions:
        reaction: Reaction = reaction
        if reaction.emoji == YES_REACTION:
            yes = reaction
            continue
        if reaction.emoji == NO_REACTION:
            no = reaction
            continue
    yes_c = 0
    no_c = 0
    if yes:
        async for user in yes.users():
            if not user.bot:
                yes_c += 1
    if no:
        async for user in no.users():
            if not user.bot:
                no_c += 1
    if yes_c > no_c:
        await callback()
        await message.edit(
            embed=Embed(
                description=f"{description}\n\nAction was approved with {yes_c}:{no_c}"))
    else:
        await message.edit(
            embed=Embed(
                description=f"{description}\n\nAction was cancelled with {yes_c}:{no_c}"))
    await message.clear_reactions()


class Polls(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.numbers = [str(i) + "\u20e3" for i in range(1, 10)]

    @group(invoke_without_command=True, case_insensitive=True)
    async def actionpoll(self, ctx: CommandContext):
        await ctx.send(
            embed=Embed(
                color=Color.red(),
                title="Syntax error on line 1 in file <discord>",
                description=f"Missing action. Can be one of "
                            f"{', '.join('`'+cmd+'`' for cmd in self.actionpoll.commands)}"))

    actionpoll: Group = actionpoll

    @actionpoll.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx: CommandContext, who: Member, reason=None):
        if who.top_role >= ctx.author.top_role:
            return await ctx.send(
                embed=Embed(
                    color=Color.red(),
                    description=f"You are lower than {who}, so you cant do this"))

        async def action():
            await who.ban(reason=reason)

        await create_action_poll(ctx, f"Ban {who} for '{reason}'?", action)

    @actionpoll.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx: CommandContext, who: Member, reason=None):
        if who.top_role >= ctx.author.top_role:
            return await ctx.send(
                embed=Embed(
                    color=Color.red(),
                    description=f"You are lower than {who}, so you cant do this"))

        async def action():
            await who.kick(reason=reason)

        await create_action_poll(ctx, f"Kick {who} for '{reason}'?", action)

    @actionpoll.command()
    @has_permissions(manage_nicknames=True)
    async def nick(self, ctx: CommandContext, who: Member, *, nick):
        if who.top_role >= ctx.author.top_role:
            return await ctx.send(
                embed=Embed(
                    color=Color.red(),
                    description=f"You are lower than {who}, so you cant do this"))

        async def action():
            await who.edit(nick=nick)

        await create_action_poll(ctx, f"Rename {who} to '{nick}'?", action)

    @command()
    async def poll(self, ctx: CommandContext, name: str, *options: str):
        if len(options) > 9:
            return await ctx.send(
                embed=Embed(
                    color=Color.red(),
                    title="Syntax error on line 1 in file <discord>",
                    description=f"More options passed then possible. {len(options)} > 9. Maybe you need to quote "
                                f"your options"))
        if len(options) < 2:
            return await ctx.send(
                embed=Embed(
                    color=Color.red(),
                    title="Syntax error on line 1 in file <discord>",
                    description=f"Too few options passed. {len(options)} < 2. As info the first argument "
                                f"is the poll **name**."))

        embed = Embed(
            color=Color.green(),
            title=name)
        for i, opt in enumerate(options):
            embed.add_field(name=self.numbers[i], value=opt, inline=False)
        mes: Message = await ctx.send(embed=embed)
        for num in self.numbers[:len(options)]:
            await mes.add_reaction(num)


def setup(bot: Bot):
    bot.add_cog(Polls(bot))
