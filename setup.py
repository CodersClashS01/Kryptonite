from pathlib import Path
from random import choice
from shutil import copy
from string import ascii_lowercase
from sys import stderr, stdout

import aioconsole as aioconsole
import aiofiles
from aioconsole.stream import NonFileStreamReader
from discord import Client, Permissions, Guild, TextChannel, Invite, Member
from discord.utils import oauth_url

motds = ["Now with 10% more errors", "CCHD is useless", "I love you sven", "Purple isn't a color",
         "it took a lot of blood and tears till we found a name, you better appreciate it",
         "Say this:\nPeter Piper picked a peck of pickled peppers. A peck of pickled peppers Peter Piper picked. If "
         "Peter Piper picked a peck of pickled peppers,Where's the peck of pickled peppers Peter Piper picked?",
         "Cryptixnite - Felix, you ain't *that* bad, but you have to improve"]

base = Path(__file__).parent
config = base / 'config.ini'
print(f"Kryptonite setup - {choice(motds)}")
print("Base path:", base)
if config.exists():
    backup = base / f"config.ini.{(''.join(choice(ascii_lowercase) for i in range(12)))}.bak"
    print(f"Config file found at {config}. A backup will be created at {backup}")
    copy(str(config), str(backup))
    print("Backup done.")

print("This setup will ask you for basic config parameters.")
print("On which IP is the bot hosted? This is needed for the web interface to work.")
ip = input("IP> ").strip()
print("Also we need a MySQL db on localhost. Please set one up.")
print("We need an user with access to a db. One example setup script would be the following: ")
print()
with open('create_user.sql') as fp:
    print(fp.read())
print()
print("This would give you the data")
print()
print("host: localhost")
print("user: codeclash")
print("password: codeclash")
print("database: codeclash")
print()
print("Now we need that data.")
mysql_host = input("MYSQL>Host> ").strip()
mysql_user = input("MYSQL>User> ").strip()
mysql_pass = input("MYSQL>Pass> ").strip()
mysql_db = input("MYSQL>Database> ").strip()

print("We need the bot token. Retrieve one at https://discordapp.com/developers/applications/me")
print("IMPORTANT: use the bot TOKEN not the SECRET. You need to create a bot user for that.")
token = input("Token> ").strip()
print("Another thing we need is a config in the applications settings.")
print("Please add")
print(f"        http://{ip}:5000/callback/")
print("as redirect uri.")
print("While you are busy with that we are trying to log in with your bot token.")

client = Client()

secret: str = None
guild: Guild = None
owner: Member = None
astdin: NonFileStreamReader = None


async def upload_emojis():
    emoji_base = base / 'emojis'
    for emoji in emoji_base.glob("*.png"):
        async with aiofiles.open(str(emoji), 'rb') as fp:
            data = await fp.read()
        await guild.create_custom_emoji(name=emoji.name[:-4], image=data)


async def save_config():
    async with aiofiles.open('config.ini', 'w') as fp:
        await fp.write(f"""
[general]
address = {ip.split(":")[0]}:5000

[discord]
TOKEN = {token}
SECRET = {secret}
game = @Kryptonite help


[mysql]
host = {mysql_host}
user = {mysql_user}
password = {mysql_pass}
database = {mysql_db}
""")


@client.event
async def on_ready():
    global secret, guild, owner, astdin
    astdin, _ = await aioconsole.get_standard_streams()
    async with aiofiles.open('avatar.png', 'rb') as avatar:
        logo = await avatar.read()
    await client.user.edit(username="Kryptonite", avatar=logo)

    print('Log in successfull.')
    print("Set profile picture and name")
    print('Next we need the bot SECRET. NOT the TOKEN this time.')
    print(end="Secret> ")
    stdout.flush()
    secret = (await astdin.readline())
    print("We currently don't verify the secret. We just hope you have us the correct one. If not you will see a "
          "bunch of errors in the webpanel. You might want to revisit the finished config.ini if that is the case")
    print("Next thing we need is a support guild to store required emotes. Do you already have a support guild? ")
    print("In that case, please add me with admin rights, so i can set up everything, like emojis.")
    print(f"Invite:      {oauth_url(client.user.id, permissions=Permissions.all())}")
    print("If you want me to create the guild, then enter CREATE if you want me to use an existing enter the id")
    print(end="Support Guild> ")
    stdout.flush()
    guild_id = await astdin.readline()
    if guild_id.lower() == "create":
        guild = await client.create_guild("Kryptonite Support", icon=logo)
        general: TextChannel = guild.system_channel
        invite: Invite = await general.create_invite()
        print("Please join the guild so i can give you permissions. ")
        print(f"         {invite.url}")
        print("Please give me your user id so i can contact you on discord.")
        print(end="Owner> ")
        stdout.flush()
        owner = guild.get_member(int((await astdin.readline()).strip()))
        await guild.edit(owner_id=owner.id)
    else:
        guild = client.get_guild(int(guild_id))
        print("Please give me your user id so i can contact you on discord.")
        print(end="Owner> ")
        stdout.flush()
        owner = guild.get_member(int((await astdin.readline()).strip()))
    await upload_emojis()
    await save_config()
    print("Everything is done. You can start the bot now with start.py")
    await client.logout()


try:
    client.run(token)
except IOError:
    print(f'Failed to login with "{token}"', file=stderr)
    exit(1)
