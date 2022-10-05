#!/usr/bin/env python3

import os
import sys
import logging
import logging.handlers
import discord
import Database
import CommandParser
from typing import List, Dict

# Making sure the script is not being run as module
if __name__ != "__main__":
    sys.exit('This script cannot be run as amodule, exitting...')

# Getting environmental variables
TOKEN: str | None = os.getenv('TOKEN')
CLI_CHANNEL: str | None = os.getenv('CLI_CHANNEL')
SERVER: str | None = os.getenv('SERVER')
REACTION_CHANNEL: str | None = os.getenv('REACTION_CHANNEL')
REACTION_MESSAGE: str | None = os.getenv('REACTION_MESSAGE')
ADMIN_ROLES_ARG: str | None = os.getenv('ADMIN_ROLES')
PROMPT: str | None = os.getenv('PROMPT')
DB_FILE: str | None = os.getenv('DB_FILE')
LOG_LEVEL_ARG: str | None = os.getenv('LOG_LEVEL')

if TOKEN is None:
    sys.exit('No token provided in environmental variables, exitting...')

if CLI_CHANNEL is None:
    sys.exit('No cli channel provided in environmental variables, exitting...')

if REACTION_CHANNEL is None:
    sys.exit('No message channel provided in environmental variables, exitting...')

if REACTION_MESSAGE is None:
    sys.exit('No message id provided in environmental variables, exitting...')

if SERVER is None:
    sys.exit('No server id provided in environmental variables, exitting...')

if ADMIN_ROLES_ARG is None:
    ADMIN_ROLES: List[str] = []
    print('No admin role defined in environmental variables, commands requiring privelaged access will not work')
else:
    ADMIN_ROLES = ADMIN_ROLES_ARG.split()

if PROMPT is None:
    PROMPT = '!'

if DB_FILE is None:
    DB_FILE = 'data.json'

LOG_LEVEL: int
if LOG_LEVEL_ARG == 'DEBUG':
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

# Setting up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True
intents.guild_reactions = True

# Instantiating the client
client = discord.Client(intents=intents)

# Instantiating the data store
db = Database.Database(DB_FILE)

# Instantiating the command handler/parser
cp = CommandParser.CommandParser(
    TOKEN,
    CLI_CHANNEL,
    ADMIN_ROLES,
    PROMPT,
    client,
    db
)

# Setting up logging
formatter = logging.Formatter(
    '[{asctime}] [{levelname:<8}] {name}: {message}',
    '%Y-%m-%d %H:%M:%S',
    style='{'
)

handler = logging.handlers.RotatingFileHandler(
    filename='log/debug.log',
    encoding='utf-8',
    maxBytes=32*1024*1024, # 32 mib max file size
    backupCount=1
)

handler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)

# Subscribing to events
@client.event
async def on_ready() -> None:
    print(f'Logged in as {client.user}')
    await startup_reaction_check()

@client.event
async def on_message(message) -> None:
    await cp.process(message)

@client.event
async def on_raw_reaction_add() -> None:
    pass
    # TODO: parse db.get() dict to check if user should get
    #       a role assigned based on the added reaction

@client.event
async def on_raw_reaction_remove() -> None:
    pass
    # TODO: parse db.get() dict to check if user should get
    #       a role removed based on the removed reaction

@client.event
async def on_raw_reaction_clear() -> None:
    pass
    # TODO: parse db.get() dict to check if users should get
    #       their roles removed based on the removed reactions

@client.event
async def startup_reaction_check() -> None:
    pass
    # TODO: perform a check to see if reactions changed while
    #       the program was offline, then correct difeerences
    #       using current reaction state as a base

    #async def check_reactions(self) -> None:
    #    checked_users = set()
    #
    #    channel = self.guilds[0].get_channel(REACTION_CHANNEL_ID)
    #    if channel == None: sys.exit("Channel could not be found, check settings.py")
    #
    #    try: message = await channel.fetch_message(REACTION_MESSAGE_ID)
    #    except discord.errors.NotFound: sys.exit("Message with reactions not found, check settings.py")
    #    except discord.errors.Forbidden: sys.exit("Bot needs permission to read message history")
    #    except discord.errors.HTTPException: sys.exit("Reading reaction message failed")
    #
    #    for reaction in message.reactions:
    #        emoji = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name
    #        async for user in reaction.users():
    #            await self.grant_role((REACTION_MESSAGE_ID, user.id, emoji))
    #            checked_users.add(user)
    #
    #    to_check = set(self.guilds[0].members).difference(checked_users)
    #
    #    for user in to_check:
    #        for match in REACTION_MATCH: await self.remove_role((REACTION_MESSAGE_ID, user.id, match))

# Running the client
client.run(TOKEN, log_handler=None)
