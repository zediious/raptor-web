import discord
from json import dump, dumps, load
from json.decoder import JSONDecodeError
from time import time
import logging

from asgiref.sync import sync_to_async
from threading import Thread

from raptorWeb import settings
if settings.SCRAPE_ANNOUNCEMENT:
    from gameservers.models import Server
    from raptorbot.models import Announcement, ServerAnnouncement
from raptorbot.models import DiscordMemberCount

logging.basicConfig(filename="error.log", level=logging.DEBUG)

from . import raptorbot_settings

async def get_server_roles(bot_instance):
    """
    Return role names and ids that match modpack names, keyed by their address key
    """
    server_data = Server.objects.all()
    sr_guild = bot_instance.get_guild(raptorbot_settings.DISCORD_GUILD)
    total_role_list = await sr_guild.fetch_roles()
    role_list = {}
    for server in server_data:
        for role in total_role_list:
            if role.name == server.modpack_name:
                role_list.update({
                    server.server_address.split('.')[0]: {
                        "id": role.id,
                        "name": role.name
                    }
                })
    return role_list

async def check_if_global_announcement_exists(message):
    global_announcements = Announcement.objects.all()
    for announcement in global_announcements:
        if message.author is announcement.author and message.content is announcement.message:
            return True

async def check_if_server_announcement_exists(message, server_address):
    server_announcements = ServerAnnouncement.objects.all()
    for announcement in server_announcements:
        if announcement.server is Server.objects.get(server_address = server_address):
            if message.author is announcement.author and message.content is announcement.message:
                return True

async def update_global_announcements(bot_instance):
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    places their content in a Dictionary, nested in another
    dictionary keyed by a countered number. Data is saved
    to an "announcements.json" each iteration.
    """
    channel = bot_instance.get_channel(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=100)]

    for message in messages:
        if check_if_global_announcement_exists(message) == True:
            continue
        Announcement.objects.create(
            author = str(message.author),
            message = message.content,
            date = str(message.created_at.date().strftime('%B %d %Y'))
        ).save()

async def update_all_server_announce(bot_instance):
    """
    Gets all messages from all server's selected channels, and adds any
    messages mentioning a server's role to a dictionary keyed  by the
    server. his is intended to be run once, if messages already existed
    in selected channels.
    """
    server_data = Server.objects.all()
    for server in server_data:
        if server.server_address.split('.')[0] == server.discord_announcement_channel_id:
            await update_server_announce(server.server_address, bot_instance=bot_instance)
        else:
            logging.debug(f'The server: {server.modpack_name} was not checked for messages')

async def update_server_announce(server_address, bot_instance):
    """
    Updates the announcement for a server passed as argument.
    Runs to update a server's messages when a message is sent 
    mentioning that server's role from it's selected channel.
    """
    server_key = server_address.split('.')[0]
    role_list = await get_server_roles(bot_instance=bot_instance)
    channel_instance = bot_instance.get_channel(Server.objects.get(server_address=server_address).discord_announcement_channel_id)
    messages = [message async for message in channel_instance.history(limit=200)]

    for message in messages:
        if check_if_server_announcement_exists(message, server_address) == True:
            continue
        if message.author != bot_instance.user:
            try:
                if message.author.get_role(raptorbot_settings.STAFF_ROLE_ID) != None:
                    if str(role_list[server_key]["id"]) in str(message.content):
                        ServerAnnouncement.objects.create(
                            server = Server.objects.get(server_address = server_address),
                            author = str(message.author),
                            message = message.content,
                            date = str(message.created_at.date().strftime('%B %d %Y'))
                        ).save()
            except AttributeError:
                continue

async def update_member_count(bot_instance):
    """
    Gets a count of total and online members on a
    provided Discord server, and places them in
    a dictionary. Data is saved to a "discordInfo.json"
    on each iteration.
    """
    server = bot_instance.get_guild(raptorbot_settings.DISCORD_GUILD)
    member_total = len(server.members)
    online_members = 0

    for member in server.members:

        if member.status != discord.Status.offline:
            online_members += 1
    
    await sync_to_async(DiscordMemberCount.objects.all().delete(), thread_sensitive=True)
    await sync_to_async(DiscordMemberCount.objects.create(
        total_members = member_total,
        online_members = online_members
    ).save(), thread_sensitive=True)
