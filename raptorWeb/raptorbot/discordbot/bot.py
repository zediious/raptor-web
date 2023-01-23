import discord
from discord.ext import commands
import logging

from raptorWeb import settings
from raptorbot.discordbot.util import raptorbot_settings, raptorbot_util
if settings.SCRAPE_ANNOUNCEMENT:
    from gameservers.models import Server

# Configure basic logger
logging.basicConfig(filename="error.log", level=logging.DEBUG)

# State bot intents and declare Bot instance
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
raptor_bot = commands.Bot(command_prefix='!', description=raptorbot_settings.DESCRIPTION, intents=intents)

# Define events to listen to and bot commands
@raptor_bot.event
async def on_ready():
    print(f'Logged in as {raptor_bot.user} (ID: {raptor_bot.user.id})')
    try:
        synced = await raptor_bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@raptor_bot.event
async def on_message(message):
    if settings.SCRAPE_ANNOUNCEMENT:
        channel = raptor_bot.get_channel(int(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID))
        if message.channel == channel:
            await raptorbot_util.update_global_announcements(raptor_bot)
        server_data = Server.objects.all()
        if message.author != raptor_bot.user and message.author.get_role(raptorbot_settings.STAFF_ROLE_ID) != None:
            async for server in server_data:
                if message.channel != raptor_bot.get_channel(int(server.discord_announcement_channel_id)):
                    continue
                if server.discord_modpack_role_id in str(message.content):
                    await raptorbot_util.update_server_announce(server_address=server.server_address, bot_instance=raptor_bot)
    
@raptor_bot.event
async def on_raw_message_edit(message):
    if settings.SCRAPE_ANNOUNCEMENT:
        if message.channel_id == raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID:
                await raptorbot_util.update_global_announcements(raptor_bot)
        server_queryset = Server.objects.filter(discord_announcement_channel_id = message.channel_id)
        if server_queryset != None:
            server = await server_queryset.aget()
            await raptorbot_util.update_server_announce(server_address=server.server_address, bot_instance=raptor_bot)

@raptor_bot.event
async def on_presence_update(before, after):
    await raptorbot_util.update_member_count(raptor_bot)

@raptor_bot.tree.command(name="display_server_info")
@discord.app_commands.describe(key = "Choose a server address prefix")
async def display_server_info(interaction: discord.Interaction, key: str):
    server_data = Server.objects.all()
    async for server in server_data:
        if server.server_address.split(".")[0] == key:
            image_embed = discord.Embed(color=0x00ff00)
            image_embed.set_image(url=f"https://shadowraptor.net/media/modpack_pictures/{server.server_address.split('.')[0]}.webp")

            info_embed = discord.Embed(title=server.modpack_name, description=f"Join at: ```{server.server_address}```", color=0x00ff00, url=server.modpack_url)
            info_embed.add_field(name="\u200b", value=await raptorbot_util.strip_html(server.modpack_description), inline=False)
            info_embed.add_field(name="\u200b", value='▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬', inline=False)
            info_embed.add_field(name="\u200b", value=await raptorbot_util.strip_html(server.server_description), inline=False)
            info_embed.add_field(name="\u200b", value=f"**Rules:** https://shadowraptor.net/rules/#{server.server_address.split('.')[0]}\n**Banned Items:** https://shadowraptor.net/banneditems/#{server.server_address.split('.')[0]}\n**Vote Links:** https://shadowraptor.net/voting/#{server.server_address.split('.')[0]}")
            info_embed.add_field(name="\u200b", value=f"The server is running;```v{server.modpack_version}```\n```Make sure to read all the information at the server spawn! It contains things you should not do, as well as helpful tips```", inline=False)

            message_embeds = [image_embed, info_embed]
            await interaction.response.send_message(embeds=message_embeds)

@raptor_bot.tree.command(name="refresh_announcements")
async def refresh_announcements(interaction: discord.Interaction):
    await raptorbot_util.update_global_announcements(raptor_bot)
    await interaction.response.send_message(embed=discord.Embed(description="Announcements JSON has been refreshed from current Announcements channel", color=0x00ff00), ephemeral=True)

@raptor_bot.tree.command(name="refresh_server_announcements")
async def refresh_server_announcements(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(description="server_announcements.json is now being updated with the announcements for servers from their respective channels, going back 200 messages.", color=0x00ff00), ephemeral=True)
    await raptorbot_util.update_all_server_announce(raptor_bot)
