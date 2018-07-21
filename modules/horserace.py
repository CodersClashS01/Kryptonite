import asyncio
import random
from collections import defaultdict
from typing import List

from discord import Message, Embed, Reaction
from discord.ext.commands import Bot, command, Context as CommandContext, is_owner

from emojis import get_arsenal, EmoteArsenal


async def display_race(message: Message, horses: List[int], arsenal: EmoteArsenal):
    text = '\n'.join(f'`{horse * "="}>`{arsenal.horse}' for horse in horses)
    await message.edit(
        embed=Embed(
            description=text))


async def play_race(message: Message, arsenal: EmoteArsenal) -> List[int]:
    horses = [0 for _ in range(4)]
    while True:
        await asyncio.sleep(1)
        await display_race(message=message, horses=horses, arsenal=arsenal)
        for i in range(len(horses)):
            horses[i] = min(30, horses[i] + random.randint(1, 3))
        if any(horse == 30 for horse in horses):
            return [i for i, horse in enumerate(horses) if horse == 10]


async def filter_bot_user_reactions(reaction: Reaction):
    return [user async for user in reaction.users() if not user.bot]


class Games(object):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.numbers = [str(i) + "\u20e3" for i in range(1, 5)]
        self.arsenal = None
        self.horse_reaction = None

    async def on_ready(self):
        self.arsenal = get_arsenal(self.bot)
        self.horse_reaction = self.arsenal.horse

    @command(hidden=True)
    @is_owner()
    async def setup_emojis(self, ctx: CommandContext):
        pass

    @command()
    async def horserace(self, ctx: CommandContext):
        race: Message = await ctx.send(content='Place your bets in the next 5 seconds!')
        for number in self.numbers:
            await race.add_reaction(number)
        await asyncio.sleep(5)
        race: Message = await ctx.get_message(race.id)

        users = defaultdict(lambda: [], {
            self.numbers.index(reaction.emoji): await (filter_bot_user_reactions(reaction))
            for reaction in race.reactions if reaction.emoji in self.numbers})  # Yay for dict comprehension
        reaction_count = defaultdict(int)
        for reaction, reactors in users.items():
            for reactor in reactors:
                reaction_count[reactor] += 1
        dupe_reactors = []
        for reactor, count in reaction_count.items():
            if count > 1:
                for key, val in users.items():
                    users[key] = [u for u in val if u != reactor]
                dupe_reactors.append(reactor)
        await race.edit(
            content=f'Horserace: {", ".join(map(str,dupe_reactors))} had duplicate reactions and were excluded from '
                    f'the race ' if len(dupe_reactors) > 0 else 'Horserace')
        winners = await play_race(race, self.arsenal)
        await race.edit(
            content='\n'.join(f'Horse {self.numbers[winner]} won. ' for winner in winners))

    @command()
    async def coinflip(self, ctx: CommandContext):
        img = random.choice(["https://imgur.com/w2yJiPB.png", "https://imgur.com/2Vmdnih.png"])
        await ctx.send(embed=Embed().set_image(url=img))


def setup(bot: Bot):
    bot.add_cog(Games(bot))
