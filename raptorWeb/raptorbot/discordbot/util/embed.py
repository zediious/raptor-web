from logging import Logger, getLogger

from django.utils.html import strip_tags
from django.utils.timezone import localtime
from django.conf import settings

import discord
from discord.ext import commands

from raptorWeb.gameservers.models import Server
from raptorWeb.raptorbot.models import SentEmbedMessage

LOGGER: Logger = getLogger('raptorbot.discordbot.util.embed')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')


async def update_embeds(bot_instance: commands.Bot) -> None:
    """
    Update all sent embeds with new server information
    """
    async for saved_embed in SentEmbedMessage.objects.all():
        if saved_embed.changed_and_unedited != True:
            continue
        server = await SentEmbedMessage.objects.select_related(
            'server'
            ).aget(id = saved_embed.id)
        message_embeds: list[discord.Embed] = await craft_embed(server.server)
        channel: discord.TextChannel = bot_instance.get_channel(int(saved_embed.channel_id))
        message = await channel.fetch_message(int(saved_embed.message_id))
        await message.edit(embeds=message_embeds)
        saved_embed.modified = localtime()
        saved_embed.changed_and_unedited = False
        await saved_embed.asave()

async def craft_embed(server: Server) -> list[discord.Embed]:
    """
    Given a Server, return a list of Embeds for display. One embed
    contains a server's modpack image, the other contains information.
    """
    image_embed = discord.Embed(color=0x00ff00)
    try:
        server_image = server.modpack_picture.url
    except ValueError:
        server_image = ''
    image_embed.set_image(
        url=f"{WEB_PROTO}://{DOMAIN_NAME}{server_image}")

    info_embed = discord.Embed(
        title=server.modpack_name,
        description=f"Join at: ```{server.server_address}```",
        color=0x00ff00,
        url=server.modpack_url)
    info_embed.add_field(
        name="\u200b",
        value=await strip_html(server.modpack_description),
        inline=False)
    info_embed.add_field(
        name="\u200b",
        value='▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
        inline=False)
    info_embed.add_field(
        name="\u200b",
        value=await strip_html(server.server_description),
        inline=False)
    info_embed.add_field(
        name="\u200b",
        value=( f"**Announcements:** {WEB_PROTO}://{DOMAIN_NAME}/announcements?server={server.pk}\n"
                f"**Rules:** {WEB_PROTO}://{DOMAIN_NAME}/rules?server={server.pk}\n"
                f"**Banned Items:** {WEB_PROTO}://{DOMAIN_NAME}/banneditems?server={server.pk}\n"
                f"**Vote Links:** {WEB_PROTO}://{DOMAIN_NAME}/voting?server={server.pk}"))
    info_embed.add_field(
        name="\u200b",
        value=(f"The server is running;```v{server.modpack_version}```\n"
                "```Make sure to read all the information at the server spawn! "
                "It contains things you should not do, as well as helpful tips```"),
        inline=False)

    return [image_embed, info_embed]


async def strip_html(value: str) -> str:
    """
    Strip certain pieces of html/unicode from a value
    Calls django.utils.html.strip_tags() internally
    """
    return strip_tags(value
        ).replace('&gt;', '>'
        ).replace('&nbsp;', ' '
        ).replace('&quot;', '"'
        ).replace('&#39;', "'"
        ).replace('&ldquo;', '"'
        ).replace('&rdquo;', '"'
        ).replace('&rsquo;', "'")
