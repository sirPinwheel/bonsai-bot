import discord
import Database
from typing import List, Dict

class CommandParser():
    def __init__(
        self,
        token: str,
        cli_channel: str,
        admin_roles: list[str],
        prompt: str,
        client: discord.Client,
        db: Database.Database
    ) -> None:

        self.token: str = token
        self.cli_channel: str = cli_channel
        self.amdin_roles: list[str] = admin_roles
        self.prompt: str = prompt
        self.client: discord.Client = client
        self.db: Database.Database = db

    def is_admin_user(self, user: discord.Member) -> bool:
        for role in user.roles:
            if str(role.id) in self.amdin_roles:
                return True
        return False

    async def bind_command(self, message: discord.Message):
        if message.content.startswith("!bind"):
            arg_list: List[str] = message.content.split()
            if len(arg_list) != 3:
                if len(arg_list) == 1:
                    await message.channel.send("Usage: ``!bind <emote> <role>``")
                    return
                await message.channel.send("Error: Wrong number of arguments")
            else:
                server_roles: List[str] = [el.name for el in self.client.guilds[0].roles]

                if arg_list[2] in server_roles:
                    if not self.db.set(arg_list[1], arg_list[2]): 
                        await message.channel.send("Error: Emote already bound")
                    else:
                        await message.channel.send(f"Success: Bound reaction {arg_list[1]} to role {arg_list[2]}")
                else:
                    await message.channel.send("Error: No such role")

    async def unbind_command(self, message: discord.Message):
        if message.content.startswith("!unbind"):
            arg_list: List[str] = message.content.split()
            if len(arg_list) != 2:
                if len(arg_list) == 1:
                    await message.channel.send("Usage: ``!unbind <emote>``")
                    return
                await message.channel.send("Error: Wrong number of arguments")
            else:
                if not self.db.remove(arg_list[1]):
                    await message.channel.send("Error: No binding for this emote")
                else:
                    await message.channel.send(f"Success: Unbound emote {arg_list[1]}")

    async def show_binds(self, message: discord.Message):
        if message.content.startswith("!show") or message.content.startswith("!list"):
            binds: Dict[str, str] = self.db.get()
            to_send: str = 'Current emote -> role associations:\n'

            for element in binds:
                to_send = to_send + f"``{element} -> {binds[element]}``\n"

            await message.channel.send(to_send)

    async def parse_admin_command(self, message: discord.Message) -> None:
        # For command type messages sent by admins
        await self.bind_command(message)
        await self.unbind_command(message)
        await self.show_binds(message)

    async def parse_command(self, message: discord.Message) -> None:
        # For all command type messages
        pass

    async def parse_message(self, message: discord.Message) -> None:
        # For every message sent
        pass

    async def process(self, message: discord.Message) -> None:
        # Ignoring bot's own messages
        if message.author == self.client.user:
            return

        # Checking if message is a command
        if message.content[0] == self.prompt:
            # Check if message is sent by a privelaged user
            if self.is_admin_user(message.author):
                await self.parse_admin_command(message)
                await self.parse_command(message)
        else:
            # Parsing every message that's not a command
            await self.parse_message(message)
