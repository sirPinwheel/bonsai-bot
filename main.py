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
TOKEN = os.getenv('TOKEN')
CLI_CHANNEL = os.getenv('CLI_CHANNEL')
ADMIN_ROLES = os.getenv('ADMIN_ROLES')
PROMPT = os.getenv('PROMPT')
DB_FILE = os.getenv('DB_FILE')
LOG_LEVEL = os.getenv('LOG_LEVEL')

if TOKEN is None:
    sys.exit('No token provided in environmental variables, exitting...')
if CLI_CHANNEL is None:
    sys.exit('No cli channel provided in environmental variables, exitting...')
if ADMIN_ROLES is None:
    ADMIN_ROLES = []
    print('No admin role defined in environmental variables, commands requiring privelaged access will not work')
if PROMPT is None: PROMPT = '!'
if DB_FILE is None: DB_FILE = 'data.json'
if LOG_LEVEL == 'DEBUG': LOG_LEVEL = logging.DEBUG
else: LOG_LEVEL = logging.INFO

# Instantiating the data store
db = database.Database(DB_FILE)

# Instantiating the cli handler/parser
cp = CommandParser() #CLI_CHANNEL)

# Setting up logging
info_format = '[{asctime}] [{levelname:<8}] {name}: {message}'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(info_format, date_format, style='{')

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

# Setting up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guild_messages = True
intents.guild_reactions = True

# Instantiating the client
client = discord.Client(intents=intents)

def is_admin_user(user):
    for role in user.roles:
        if role in ADMIN_ROLES:
            return True
    return False

# Subscribing to events
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignoring bot's own messages
    if message.author == client.user:
        return
    # Checking if message comes from cli channel
    if message.channel == CLI_CHANNEL:
        # Checking if it's from a privelaged user
        if is_admin_user(message.author):
            cp.parse_message(message)
            cp.parse_command(message)
    else:
        cp.parse_message(message)

@client.event
async def on_raw_reaction_add():
    pass
    # TODO: parse db.get() dict to check if user should get
    #       a role assigned based on the added reaction

@client.event
async def on_raw_reaction_remove():
    pass
    # TODO: parse db.get() dict to check if user should get
    #       a role removed based on the removed reaction

@client.event
async def on_raw_reaction_clear():
    pass
    # TODO: parse db.get() dict to check if users should get
    #       their roles removed based on the removed reactions

@client.event
async def startup_reaction_check():
    pass
    # TODO: perform a check to see if reactions changed while
    #       the program was offline, then correct difeerences
    #       using current reaction state as a base

# Running the client
client.run(TOKEN, log_handler=None)
