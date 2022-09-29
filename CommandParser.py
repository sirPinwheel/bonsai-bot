from xmlrpc.client import Boolean
import discord
import database

class CommandParser():
    def __init__(self, token: str, cli_channel: str, admin_roles: list[str], prompt: str, client: discord.Client) -> None:
        self.token: str = token
        self.cli_channel: str = cli_channel
        self.amdin_roles: list[str] = admin_roles
        self.prompt: str = prompt
        self.client: discord.Client = client

    def is_admin_user(self, user) -> bool:
        for role in user.roles:
            if role in self.amdin_roles:
                return True
        return False

    def parse_command(self, message) -> None:
        pass

    def parse_message(self, message) -> None:
        pass

    def process(self, message) -> None:
        # Ignoring bot's own messages
        if message.author == self.client.user:
            return
        # Checking if message comes from cli channel
        if message.channel == self.CLI_CHANNEL:
            # Checking if it's from a privelaged user
            if self.is_admin_user(message.author):
                self.parse_message(message)
                self.parse_command(message)
        else:
            self.parse_message(message)