from typing import Optional

from django.conf import settings

import discord
from discord.ext import commands

from raptorWeb.raptorbot.models import GlobalAnnouncement

SCRAPE_SERVER_ANNOUNCEMENT: bool = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')
GLOBAL_ANNOUNCEMENT_CHANNEL_ID: int = getattr(settings, 'GLOBAL_ANNOUNCEMENT_CHANNEL_ID')
STAFF_ROLE_ID: int = getattr(settings, 'STAFF_ROLE_ID')

if SCRAPE_SERVER_ANNOUNCEMENT:
    from raptorWeb.gameservers.models import Server
    from raptorWeb.raptorbot.models import ServerAnnouncement


async def check_if_global_announcement_exists(message: discord.Message) -> Optional[bool | str]:
    """
    Check if a Global Announcement with matching author and content exists, and return
    True if so. If a Global Announcment with the same author and date, but not message 
    exists, will return a string "edited"
    """
    global_announcements: GlobalAnnouncement.objects = GlobalAnnouncement.objects.all()

    async for announcement in global_announcements:
        if (str(message.author) == str(announcement.author)
        and str(message.content) == str(announcement.message)):
            return True

        if (str(message.author) == str(announcement.author)
        and str(message.content) != str(announcement.message)
        and str(message.created_at) == str(announcement.date)):
            return "edited"


async def check_if_server_announcement_exists(message: discord.Message, modpack_name: str) -> Optional[bool | str]:
    """
    Check if a Server Announcement with matching author, content  and server exists, and 
    return True if so. If a Server Announcment with the same author, date, and server but   
    not message exists, will return a string "edited"
    """
    server_announcements: ServerAnnouncement.objects = ServerAnnouncement.objects.all()

    async for announcement in server_announcements:
        announcement_server: Server = await ServerAnnouncement.objects.select_related(
            'server'
            ).aget(id = announcement.id)

        if announcement_server.server.modpack_name == modpack_name:
            if (str(message.author) == str(announcement.author)
            and str(message.content) == str(announcement.message)):
                return True

            if (str(message.author) == str(announcement.author)
            and str(message.content) != str(announcement.message)
            and str(message.created_at) == str(announcement.date)):
                return "edited"


async def update_all_server_announce(bot_instance: commands.Bot) -> None:
    """
    Runs update_server_announce() against all Servers in database.
    """
    server_data: Server.objects = Server.objects.all()

    async for server in server_data:
        await update_server_announce(
            server.modpack_name,
            bot_instance=bot_instance)


async def update_global_announcements(bot_instance: commands.Bot) -> None:
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    create Announcement objects for each message.
    """
    channel: discord.guild.GuildChannel = bot_instance.get_channel(GLOBAL_ANNOUNCEMENT_CHANNEL_ID)
    messages: list[discord.Message] = [message async for message in channel.history(limit=100)]

    for message in messages:
        exists: bool | str = await check_if_global_announcement_exists(message)
        if exists == True:
            continue

        elif exists == None:
            await GlobalAnnouncement.objects.acreate(
                author = str(message.author),
                message = message.content,
                date = message.created_at
            )

        elif exists == "edited":
            replacing_announcement: GlobalAnnouncement = await GlobalAnnouncement.objects.aget(
                author=message.author,
                date=message.created_at)

            await GlobalAnnouncement.objects.filter(
                author=message.author,
                date=message.created_at).adelete()

            await GlobalAnnouncement.objects.acreate(
                id = replacing_announcement.id,
                author = str(replacing_announcement.author),
                message = message.content,
                date = replacing_announcement.date
            )


async def update_server_announce(modpack_name: str, bot_instance: commands.Bot):
    """
    Updates the announcements for a server passed as argument.
    Creates a ServerAnnouncement keyed to iterated server for each
    message in the Server's Discord Channel that contains a role 
    mention of a role matching a Server's modpack_name field.
    Will delete edited messages and recreate with new message content
    while retaining previous date.
    """
    server_in_db: Server = await Server.objects.aget(modpack_name=modpack_name)
    channel_instance: discord.guild.GuildChannel = bot_instance.get_channel(
        int(server_in_db.discord_announcement_channel_id))

    if (channel_instance != None and server_in_db.discord_announcement_channel_id != "0"
    and server_in_db.discord_modpack_role_id != "0"):
        messages: list[discord.Message] = [message async for message in channel_instance.history(limit=500)]

        for message in messages:
            exists: bool | str = await check_if_server_announcement_exists(message, modpack_name)

            if exists == True:
                continue

            elif exists == None:
                if message.author != bot_instance.user:
                    try:
                        if (message.author.get_role(STAFF_ROLE_ID) != None
                        and str(server_in_db.discord_modpack_role_id) in str(message.content)):
                            await ServerAnnouncement.objects.acreate(
                                server = await Server.objects.aget(modpack_name = modpack_name),
                                author = str(message.author),
                                message = message.content,
                                date = message.created_at
                            )

                    except AttributeError:
                        continue

            elif exists == "edited":
                replacing_announcement: ServerAnnouncement = await ServerAnnouncement.objects.aget(
                    author=message.author,
                    date=message.created_at)

                await ServerAnnouncement.objects.filter(author=message.author, date=message.created_at).adelete()

                await ServerAnnouncement.objects.acreate(
                    id = replacing_announcement.id,
                    server = await Server.objects.aget(modpack_name = modpack_name),
                    author = replacing_announcement.author,
                    message = message.content,
                    date = replacing_announcement.date
                )
