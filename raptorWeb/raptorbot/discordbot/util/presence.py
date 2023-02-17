from logging import Logger, getLogger

from django.conf import settings

import discord
from discord.ext import commands

from raptorWeb.raptorbot.models import DiscordGuild

LOGGER: Logger = getLogger('raptorbot.discordbot.util')
GLOBAL_ANNOUNCEMENT_CHANNEL_ID: int = getattr(settings, 'GLOBAL_ANNOUNCEMENT_CHANNEL_ID')
DISCORD_GUILD: int = getattr(settings, 'DISCORD_GUILD')


async def update_invite_link(bot_instance: commands.Bot) -> None:
    """
    If a DiscordGuild does not have an invite_link, create one and
    add it to the class attribute invite_link for the DiscordGuild
    """
    async def _create_invite_link(bot_instance: commands.Bot) -> discord.Invite:
        """
        Create discord invite link
        """
        channel: discord.guild.GuildChannel = bot_instance.get_channel(GLOBAL_ANNOUNCEMENT_CHANNEL_ID)
        return await channel.create_invite()

    server: discord.Guild = bot_instance.get_guild(DISCORD_GUILD)

    try:
        guild_set: DiscordGuild.objects = DiscordGuild.objects.filter(guild_id = server.id)
        guild: DiscordGuild = await guild_set.afirst()

        if not guild.invite_link:
            invite: discord.Invite = await _create_invite_link(bot_instance)

            await DiscordGuild.objects.aupdate(
                guild_name = server.name,
                guild_id = server.id,
                invite_link=invite)

    except DiscordGuild.DoesNotExist:
        LOGGER.info("There was an irrecoverable error in on_presence_update()")


async def update_member_count(bot_instance: commands.Bot) -> None:
    """
    Gets a count of total and online members on a
    provided Discord server, and create a DiscordGuild
    with the guilds name, ID, and gathered member info.
    If DiscordGuild exists, delete and re-create with
    existing guild_name and guild_id
    """
    server: discord.Guild = bot_instance.get_guild(DISCORD_GUILD)
    member_total: int = len(server.members)
    online_members: int = 0

    for member in server.members:
        if member.status != discord.Status.offline:
            online_members += 1
    
    try:
        await DiscordGuild.objects.filter(guild_id = server.id).aupdate(
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
