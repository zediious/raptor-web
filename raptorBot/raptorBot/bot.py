import discord
from discord.ext import commands
import logging
from json import load

from util import raptorbot_settings, raptorbot_util

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
    channel = raptor_bot.get_channel(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID)
    if message.channel == channel:
        await raptorbot_util.update_global_announcements(raptor_bot)
    server_data = dict(load(open('../../raptorWeb/server_data.json', "r")))
    role_list = await raptorbot_util.get_server_roles(raptor_bot)
    for announce_channel in raptorbot_settings.SERVER_ANNOUNCEMENT_CHANNEL_IDS:
        if message.author != raptor_bot.user:
            if message.channel == raptor_bot.get_channel(raptorbot_settings.SERVER_ANNOUNCEMENT_CHANNEL_IDS[announce_channel]):
                try:
                    if message.author.get_role(raptorbot_settings.STAFF_ROLE_ID) != None:
                        for role in role_list:
                            try:
                                if str(role_list[role]["id"]) in str(message.content) and str(role_list[role]["name"]) == server_data[announce_channel]["modpack_name"]:
                                    raptorbot_util.update_server_announce(server_key=server_data[announce_channel]["address"].split('.')[0], bot_instance=raptor_bot)
                            except KeyError:
                                try: 
                                    logging.debug(f'{e}\nA KeyError occured, debug information below\n\nMessage channel: {message.channel}\n\nRole list: {role_list}\n\nCurrent server info: {server_data[announce_channel]}')
                                    break
                                except:
                                    logging.debug("An error occured logging a previous error.")
                                    break
                except AttributeError as e:
                    try: 
                        logging.debug(f'{e}\nAn Attribute Error occured, debug information below\n\nMessage channel: {message.channel}\n\nRole list: {role_list}\n\nCurrent server info: {server_data[announce_channel]}')
                        break
                    except:
                        logging.debug("An error occured logging a previous error.")
                        break

@raptor_bot.event
async def on_raw_message_edit(message):
    channel = raptor_bot.get_channel(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID)
    try:
        if message.channel == channel:
            await raptorbot_util.update_global_announcements(raptor_bot)
    except AttributeError:
        if message.channel_id == raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID:
            await raptorbot_util.update_global_announcements(raptor_bot)

@raptor_bot.event
async def on_presence_update(before, after):
    await raptorbot_util.update_member_count(raptor_bot)

@raptor_bot.tree.command(name="display_server_info")
@discord.app_commands.describe(key = "Choose a server address prefix")
async def display_server_info(interaction: discord.Interaction, key: str):
    server_data = dict(load(open('../../raptorWeb/server_data.json', "r")))
    for server in server_data:

        if server_data[server]["address"].split(".")[0] == key:
            image_embed = discord.Embed(color=0x00ff00)
            image_embed.set_image(url=f"https://shadowraptor.net/media/modpack_pictures/{server_data[server]['address'].split('.')[0]}.webp")

            info_embed = discord.Embed(title=server_data[server]["modpack_name"], description=f"Join at: ```{server_data[server]['address']}```", color=0x00ff00, url=server_data[server]["modpack_url"])
            info_embed.add_field(name="\u200b", value=server_data[server]['modpack_description'], inline=False)
            info_embed.add_field(name="\u200b", value=server_data[server]['server_description'], inline=False)
            info_embed.add_field(name="\u200b", value=f"**Rules:** https://shadowraptor.net/rules/#{server_data[server]['address'].split('.')[0]}\n**Banned Items:** https://shadowraptor.net/banneditems/#{server_data[server]['address'].split('.')[0]}\n**Vote Links:** https://shadowraptor.net/voting/#{server_data[server]['address'].split('.')[0]}")
            info_embed.add_field(name="\u200b", value=f"The server is running;```v{server_data[server]['modpack_version']}```\n```Make sure to read all the information at the server spawn! It contains things you should not do, as well as helpful tips```", inline=False)

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

# Run the bot
raptor_bot.run(raptorbot_settings.TOKEN)
