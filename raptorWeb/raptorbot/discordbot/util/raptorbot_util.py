from logging import getLogger

from django.utils.html import strip_tags
from django.conf import settings

import discord

from raptorWeb.raptorbot.models import GlobalAnnouncement
from raptorWeb.raptorbot.models import DiscordGuild

SCRAPE_SERVER_ANNOUNCEMENT = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')
GLOBAL_ANNOUNCEMENT_CHANNEL_ID = getattr(settings, 'GLOBAL_ANNOUNCEMENT_CHANNEL_ID')
DISCORD_GUILD = getattr(settings, 'DISCORD_GUILD')
STAFF_ROLE_ID = getattr(settings, 'STAFF_ROLE_ID')

if SCRAPE_SERVER_ANNOUNCEMENT:
    from raptorWeb.gameservers.models import Server
    from raptorWeb.raptorbot.models import ServerAnnouncement

LOGGER = getLogger('discordbot.util')

async def check_if_global_announcement_exists(message):
    """
    Check if a Global Announcement with matching author and content exists, and return
    True if so. If a Global Announcment with the same author and date, but not message 
    exists, will return a string "edited"
    """
    global_announcements = GlobalAnnouncement.objects.all()
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

async def strip_html(value):
    """
    Strip certain pieces of html/unicode from a value
    Calls django.utils.html.strip_tags() internally
    """
    return strip_tags(value).replace('&gt;', '>').replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'")

async def update_all_server_announce(bot_instance):
    """
    Runs update_server_announce() against all Servers in database.
    """
    server_data = Server.objects.all()
    async for server in server_data:
            await update_server_announce(server.server_address, bot_instance=bot_instance)

async def update_global_announcements(bot_instance):
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    create Announcement objects for each message.
    """
    channel = bot_instance.get_channel(GLOBAL_ANNOUNCEMENT_CHANNEL_ID)
    messages = [message async for message in channel.history(limit=100)]

    for message in messages:
        exists = await check_if_global_announcement_exists(message)
        if exists == True:
            continue
        elif exists == None:
            await GlobalAnnouncement.objects.acreate(
                author = str(message.author),
                message = message.content,
                date = message.created_at
            )
        elif exists == "edited":
            replacing_announcement = await GlobalAnnouncement.objects.aget(author=message.author, date=message.created_at)
            await GlobalAnnouncement.objects.filter(author=message.author, date=message.created_at).adelete()
            await GlobalAnnouncement.objects.acreate(
                id = replacing_announcement.id,
                author = str(replacing_announcement.author),
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
    server = bot_instance.get_guild(DISCORD_GUILD)
    member_total = len(server.members)
    online_members = 0

    for member in server.members:
        if member.status != discord.Status.offline:
            online_members += 1
    
    try:
        replacing_guild = await DiscordGuild.objects.aget(guild_id = server.id)
        await DiscordGuild.objects.filter(guild_id = server.id).adelete()
        await DiscordGuild.objects.acreate(
            guild_name = replacing_guild.guild_name,
            guild_id = replacing_guild.guild_id,
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

async def update_server_announce(server_address, bot_instance):
    """
    Updates the announcements for a server passed as argument.
    Creates a ServerAnnouncement keyed to iterated server for each
    message in the Server's Discord Channel that contains a role 
    mention of a role matching a Server's modpack_name field.
    Will delete edited messages and recreate with new message content
    while retaining previous date.
    """
    server_in_db = await Server.objects.aget(server_address=server_address)
    channel_instance = bot_instance.get_channel(int(server_in_db.discord_announcement_channel_id))
    if channel_instance != None and server_in_db.discord_announcement_channel_id != "0" and server_in_db.discord_modpack_role_id != "0":
        messages = [message async for message in channel_instance.history(limit=500)]
        for message in messages:
            exists = await check_if_server_announcement_exists(message, server_address)
            if exists == True:
                continue
            elif exists == None:
                if message.author != bot_instance.user:
                    try:
                        if message.author.get_role(STAFF_ROLE_ID) != None and str(server_in_db.discord_modpack_role_id) in str(message.content):
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
                    id = replacing_announcement.id,
                    server = await Server.objects.aget(server_address = server_address),
                    author = replacing_announcement.author,
                    message = message.content,
                    date = replacing_announcement.date
                )
