from logging import Logger, getLogger

import discord
from discord.ext import commands

LOGGER: Logger = getLogger('raptorbot.discordbot.util.messages')

async def delete_messages(bot_instance: commands.Bot, messages_string: str) -> None:
    """
    Delete all messages in DiscordbotTasks messages_to_delete field
    """
    messages = messages_string[:-1].split(',')
    for message in messages:
        message_details = message.replace('(', '').replace(')', '').split('.')
        channel: discord.TextChannel = bot_instance.get_channel(int(message_details[1]))
        message = await channel.fetch_message(int(message_details[0]))
        await message.delete()
