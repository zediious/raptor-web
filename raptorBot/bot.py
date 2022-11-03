import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from json import dumps, load

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

DESCRIPTION = "I do work for the ShadowRaptorMC website!"
DISCORD_GUILD = 740388741079760937
ANNOUNCEMENT_CHANNEL = 741015006480564254

async def update_announcements(message):
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    places their content in a Dictionary, nested in another
    dictionary keyed by a countered number. Data is saved
    to an "announcements.json" each iteration.
    """
    channel = raptor_bot.get_channel(ANNOUNCEMENT_CHANNEL)
    try:

        if message.channel == channel:

            messages = [message async for message in channel.history(limit=30)]
            announcements = {}

            key = 0
            for message in messages:
                announcements.update({
                    "message{}".format(key): {
                        "author": str(message.author),
                        "message": message.content,
                        "date": str(message.created_at.date().strftime('%B %d %Y'))
                        }
                })
                key += 1

            announcementsJSON = open("../raptorWeb/announcements.json", "w")
            announcementsJSON.write(dumps(announcements, indent=4))
            announcementsJSON.close()

    except AttributeError:

        if message.channel_id == ANNOUNCEMENT_CHANNEL:

            messages = [message async for message in channel.history(limit=30)]
            announcements = {}

            key = 0
            for message in messages:
                announcements.update({
                    "message{}".format(key): {
                        "author": str(message.author),
                        "message": message.content,
                        "date": str(message.created_at.date().strftime('%B %d %Y'))
                        }
                })
                key += 1

            announcementsJSON = open("../raptorWeb/announcements.json", "w")
            announcementsJSON.write(dumps(announcements, indent=4))
            announcementsJSON.close()

async def update_member_count():
    """
    Gets a count of total and online members on a
    provided Discord server, and places them in
    a dictionary. Data is saved to a "discordInfo.json"
    on each iteration.
    """
    server = raptor_bot.get_guild(DISCORD_GUILD)
    member_total = len(server.members)
    online_members = 0

    for member in server.members:

        if member.status != discord.Status.offline:
            online_members += 1

    discord_info = {
        "totalMembers": member_total,
        "onlineMembers": online_members
    }

    membersJSON = open("../raptorWeb/discordInfo.json", "w")
    membersJSON.write(dumps(discord_info, indent=4))
    membersJSON.close()

# State bot intents and declare Bot instance
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
raptor_bot = commands.Bot(command_prefix='!', description=DESCRIPTION, intents=intents)

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
    await update_announcements(message)

@raptor_bot.event
async def on_raw_message_edit(message):
    await update_announcements(message)

@raptor_bot.event
async def on_presence_update(before, after):
    await update_member_count()

@raptor_bot.tree.command(name="display_server_info")
@discord.app_commands.describe(key = "Choose a server address prefix")
async def display_server_info(interaction: discord.Interaction, key: str):
    server_data = dict(load(open('../raptorWeb/server_data.json', "r")))
    for server in server_data:

        if server_data[server]["address"].split(".")[0] == key:
            server_embed = discord.Embed(title=server_data[server]["modpack_name"], description=f"Join at: ```{server_data[server]['address']}```", color=0x00ff00, url=server_data[server]["modpack_url"])
            server_embed.add_field(name="Modpack Description", value=server_data[server]['modpack_description'], inline=False)
            server_embed.add_field(name="Server Description", value=server_data[server]['server_description'], inline=False)
            server_embed.add_field(name="~~~",
            value=f"Rules: https://shadowraptor.net/rules/#{server_data[server]['address'].split('.')[0]}\nBanned Items: https://shadowraptor.net/banneditems/#{server_data[server]['address'].split('.')[0]}\nVote Links: https://shadowraptor.net/voting/#{server_data[server]['address'].split('.')[0]}")
            server_embed.add_field(name="~~~", value=f"The server is running ```v{server_data[server]['modpack_version']}```", inline=False)
            server_embed.add_field(name="~~~", value="```Make sure to read all the information at the server spawn! It contains things you should not do, as well as helpful tips```", inline=False)
            server_embed.set_image(url=f"https://shadowraptor.net/media/modpack_pictures/{server_data[server]['address'].split('.')[0]}.webp")

            await interaction.response.send_message(embed=server_embed)

# Run the bot
raptor_bot.run(TOKEN)
