from discord.ext import commands
from discord.ext.commands import Context as CommandContext

from database import AdminModel


def admin_perms(label: int):
    def predicate(ctx: CommandContext):
        return AdminModel.get_or_insert(ctx.author).permissions <= label

    return commands.check(predicate)
