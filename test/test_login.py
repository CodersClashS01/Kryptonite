import os

from discord.ext.commands import Bot

from utils import load_all_modules


class Cog(object):
    def __init__(self, client: Bot):
        self.client: Bot = client

    async def on_ready(self):
        print('On ready')
        await self.client.close()


def test_login():
    from main import client
    client.add_cog(Cog(client))
    load_all_modules(client, module_folder='../modules', module_package='modules')
    client.run(os.environ.get('test_token', 'no_token'))
