import os
import sys
import discord

PROMPT = os.getenv('PROMPT')
TOKEN = os.getenv('TOKEN')

if PROMPT is None:
    PROMPT = '!'

if TOKEN is None:
    sys.exit('No token provided in environmental variables')

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

    client.run(TOKEN)

if __name__ == "__main__":
    main()
