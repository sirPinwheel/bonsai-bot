#!/usr/bin/env python3

import os
import sys
import logging
import logging.handlers
import discord
import database
import CommandParser

# Making sure the script is not being run as module
if __name__ != "__main__":
    sys.exit('This script cannot be run as amodule, exitting...')

# Getting environmental variables
TOKEN: str | None = os.getenv('TOKEN')
CLI_CHANNEL: str | None = os.getenv('CLI_CHANNEL')
ADMIN_ROLES: list[str] | None = os.getenv('ADMIN_ROLES').split()
PROMPT: str | None = os.getenv('PROMPT')
DB_FILE: str | None = os.getenv('DB_FILE')
LOG_LEVEL: str | None = os.getenv('LOG_LEVEL')

if TOKEN is None:
    sys.exit('No token provided in environmental variables, exitting...')

if CLI_CHANNEL is None:
    sys.exit('No cli channel provided in environmental variables, exitting...')

if ADMIN_ROLES is None:
    ADMIN_ROLES = []
    print('No admin role defined in environmental variables, commands requiring privelaged access will not work')

if PROMPT is None:
    PROMPT = '!'

if DB_FILE is None:
    DB_FILE = 'data.json'

if LOG_LEVEL == 'DEBUG':
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
db = database.Database(DB_FILE)

# Instantiating the command handler/parser
cp = CommandParser(
    TOKEN,
    CLI_CHANNEL,
    ADMIN_ROLES,
    PROMPT,
    client)

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

@client.event
async def on_message(message) -> None:
    cp.process(message)

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

# Running the client
client.run(TOKEN, log_handler=None)
