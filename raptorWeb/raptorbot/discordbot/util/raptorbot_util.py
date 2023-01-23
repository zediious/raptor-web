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
from raptorbot.models import DiscordGuild

logging.basicConfig(filename="error.log", level=logging.DEBUG)

from raptorbot.discordbot.util import raptorbot_settings

async def get_server_roles(bot_instance):
    """
    Return role names and ids that match modpack names, keyed by their address key
    """
    server_data = Server.objects.all()
    sr_guild = bot_instance.get_guild(raptorbot_settings.DISCORD_GUILD)
    total_role_list = await sr_guild.fetch_roles()
    role_list = {}
    async for server in server_data:
        for role in total_role_list:
            if role.name == server.modpack_name:
                role_list.update({
                    server.modpack_name: {
                        "id": role.id,
                        "name": role.name
                    }
                })
    return role_list

async def check_if_global_announcement_exists(message):
    """
    Check if a Global Announcement with matching author and content exists, and return
    True if so. If a Global Announcment with the same author and date, but not message 
    exists, will return a string "edited"
    """
    global_announcements = Announcement.objects.all()
    async for announcement in global_announcements:
        if str(message.author) == str(announcement.author) and str(message.content) == str(announcement.message):
            return True
        if str(message.author) == str(announcement.author) and str(message.content) != str(announcement.message) and str(message.created_at) == str(announcement.date):
            return "edited"

async def check_if_server_announcement_exists(message, server_address):
    """
    Check if a Server Announcement with matching author, content  and server exists, and 
    return True if so. If a Server Announcment with the same author, date, and server but   
    not message exists, will return a string "edited"
    """
    server_announcements = ServerAnnouncement.objects.all()
    async for announcement in server_announcements:
        announcement_server = await ServerAnnouncement.objects.select_related('server').aget(id = announcement.id)
        if announcement_server.server.server_address == server_address:
            if str(message.author) == str(announcement.author) and str(message.content) == str(announcement.message):
                return True
            if str(message.author) == str(announcement.author) and str(message.content) != str(announcement.message) and str(message.created_at) == str(announcement.date):
                return "edited"

async def update_global_announcements(bot_instance):
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    create Announcement objects for each message.
    """
    channel = bot_instance.get_channel(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=100)]

    for message in messages:
        exists = await check_if_global_announcement_exists(message)
        if exists == True:
            continue
        elif exists == None:
            await Announcement.objects.acreate(
                author = str(message.author),
                message = message.content,
                date = message.created_at
            )
        elif exists == "edited":
            replacing_announcement = await Announcement.objects.aget(author=message.author, date=message.created_at)
            await Announcement.objects.filter(author=message.author, date=message.created_at).adelete()
            await Announcement.objects.acreate(
                author = str(replacing_announcement.author),
                message = message.content,
                date = replacing_announcement.date
            )
            

async def update_all_server_announce(bot_instance):
    """
    Runs update_server_announce() against all Servers in database.
    """
    server_data = Server.objects.all()
    async for server in server_data:
            await update_server_announce(server.server_address, bot_instance=bot_instance)

async def update_server_announce(server_address, bot_instance):
    """
    Updates the announcements for a server passed as argument.
    Creates a ServerAnnouncement keyed to iterated server for each
    message in the Server's Discord Channel that contains a role 
    mention of a role matching a Server's modpack_name field.
    Will delete edited messages and recreate with new message content
    while retaining previous date.
    """
    role_list = await get_server_roles(bot_instance=bot_instance)
    server_in_db = await Server.objects.aget(server_address=server_address)
    channel_instance = bot_instance.get_channel(int(server_in_db.discord_announcement_channel_id))
    if channel_instance != None:
        messages = [message async for message in channel_instance.history(limit=500)]

        for message in messages:
            exists = await check_if_server_announcement_exists(message, server_address)
            if exists == True:
                continue
            elif exists == None:
                if message.author != bot_instance.user:
                    try:
                        if message.author.get_role(raptorbot_settings.STAFF_ROLE_ID) != None and str(role_list[server_in_db.modpack_name]["id"]) in str(message.content):
                                await ServerAnnouncement.objects.acreate(
                                    server = await Server.objects.aget(server_address = server_address),
                                    author = str(message.author),
                                    message = message.content,
                                    date = message.created_at
                                )
                    except AttributeError:
                        continue
            elif exists == "edited":
                replacing_announcement = await ServerAnnouncement.objects.aget(author=message.author, date=message.created_at)
                await ServerAnnouncement.objects.filter(author=message.author, date=message.created_at).adelete()
                await ServerAnnouncement.objects.acreate(
                    server = await Server.objects.aget(server_address = server_address),
                    author = replacing_announcement.author,
                    message = message.content,
                    date = replacing_announcement.date
                )


async def update_member_count(bot_instance):
    """
    Gets a count of total and online members on a
    provided Discord server, and create a DiscordGuild
    with the guilds name, ID, and gathered member info.
    If DiscordGuild exists, delete and re-create with
    existing guild_name and guild_id
    """
    server = bot_instance.get_guild(raptorbot_settings.DISCORD_GUILD)
    member_total = len(server.members)
    online_members = 0

    for member in server.members:

        if member.status != discord.Status.offline:
            online_members += 1
    
    try:
        replacing_guild = await DiscordGuild.objects.aget(guild_id = server.id)
        await DiscordGuild.objects.filter(guild_id = server.id).adelete()
        await DiscordGuild.objects.acreate(
            guild_name = replacing_guild.name,
            guild_id = replacing_guild.id,
            total_members = member_total,
            online_members = online_members
        )
    except DiscordGuild.DoesNotExist:
        await DiscordGuild.objects.acreate(
            guild_name = server.name,
            guild_id = server.id,
            total_members = member_total,
            online_members = online_members
        )


