from logging import Logger, getLogger

from django.utils.html import strip_tags
from django.conf import settings

import discord

from raptorWeb.gameservers.models import Server

LOGGER: Logger = getLogger('raptorbot.discordbot.util')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')


async def craft_embed(server: Server) -> list[discord.Embed]:
    """
    Given a Server, return a list of Embeds for display. One embed
    contains a server's modpack image, the other contains information.
    """
    image_embed = discord.Embed(color=0x00ff00)
    image_embed.set_image(
        url=f"{WEB_PROTO}://{DOMAIN_NAME}{server.modpack_picture.url}")

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
        value=(f"**Rules:** {WEB_PROTO}://{DOMAIN_NAME}/rules/#{server.pk}\n"
                f"**Banned Items:** {WEB_PROTO}://{DOMAIN_NAME}/banneditems/#{server.pk}\n"
                f"**Vote Links:** {WEB_PROTO}://{DOMAIN_NAME}/voting/#{server.pk}"))
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
