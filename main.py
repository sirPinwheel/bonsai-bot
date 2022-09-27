#!/usr/bin/env python3

import os
import sys
import logging
import logging.handlers
import discord

# Getting environmental variables
PROMPT = os.getenv('PROMPT') # defaults to '!'
TOKEN = os.getenv('TOKEN')
LOG_LEVEL = os.getenv('LOG_LEVEL')

if PROMPT is None:
    PROMPT = '!'

if TOKEN is None:
    sys.exit('No token provided in environmental variables')

if LOG_LEVEL == 'DEBUG':
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

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


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith(PROMPT):
            await message.channel.send('Hello!')

    client.run(TOKEN, log_handler=None)

if __name__ == "__main__":
    main()
