import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from json import dump, dumps, load
from os.path import getmtime
from time import time

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

DESCRIPTION = "I do work for the ShadowRaptorMC website!"
DISCORD_GUILD = 740388741079760937
ANNOUNCEMENT_CHANNEL = 741015006480564254
STAFF_ROLE_ID = 937891209291120660

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

async def update_server_announcements(message):
    """
    Get all messages mentioning roles associated with 
    the list of Server Modals, and places them
    in a dictionary keyed by the Server address key.
    """
    if message.author.get_role(STAFF_ROLE_ID) != None:
        try:
            lock_time = time() - getmtime('update_server_announcements.LOCK')
        
            if lock_time >= 10: 
                announcement_dict = {}
                try:
                    with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
                        announcement_dict = load(announcement_json)
                except:
                    with open("../raptorWeb/server_announcements.json", "w") as create_file:
                        create_file.write('{}')
                        print('Created empty server_announcements.json')
                    with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
                        announcement_dict = load(announcement_json)
                with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
                    server_data = dict(load(open('../raptorWeb/server_data.json', "r")))
                    sr_guild = raptor_bot.get_guild(DISCORD_GUILD)
                    total_role_list = await sr_guild.fetch_roles()
                    announcement_json.seek(0)
                    role_list = {}
                    # Get role names and ids that match modpack names, keyed by their address key
                    for server in server_data:
                        for role in total_role_list:
                            if role.name == str(f'{server_data[server]["modpack_name"]}'):
                                role_list.update({
                                    server_data[server]["address"].split('.')[0]: {
                                        "id": role.id,
                                        "name": role.name
                                    }
                                })
                    # Check if message contains a mention of roles found above, if a match is found it is saved
                    for server in server_data:
                        for role in role_list:
                            if str(role_list[role]["id"]) in str(message.content) and str(role_list[role]["name"]) == server_data[server]["modpack_name"]:
                                current_time = time()
                                try:
                                    announcement_dict[server_data[server]["address"].split('.')[0]].update({
                                        f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
                                            "author": str(message.author),
                                            "message": message.content,
                                            "date": str(message.created_at.date().strftime('%B %d %Y'))
                                        }
                                    })
                                # If a dictionary keyed by server role/modpack name doesn't exist, create it first.
                                except KeyError as e:
                                    announcement_dict.update({
                                        server_data[server]["address"].split('.')[0]: {}
                                    })
                                    announcement_dict[server_data[server]["address"].split('.')[0]].update({
                                        f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
                                            "author": str(message.author),
                                            "message": message.content,
                                            "date": str(message.created_at.date().strftime('%B %d %Y'))
                                        }
                                    })


                    dump(announcement_dict, announcement_json, indent=4)

                with open('update_server_announcements.LOCK', 'w') as lock_file:
                    lock_file.write("update_server_announcements function LOCK File. Do not modify manually.")

            else:
                print("Not enough time has passed to update server announcements")

        except FileNotFoundError as e:
            print(f"{e}\n")
            print("update_server_announcements.LOCK file not found. Create a file with this exact name in the same directory as bot.py.")


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
    await update_server_announcements(message)

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
            image_embed = discord.Embed(color=0x00ff00)
            image_embed.set_image(url=f"https://shadowraptor.net/media/modpack_pictures/{server_data[server]['address'].split('.')[0]}.webp")

            info_embed = discord.Embed(title=server_data[server]["modpack_name"], description=f"Join at: ```{server_data[server]['address']}```", color=0x00ff00, url=server_data[server]["modpack_url"])
            info_embed.add_field(name="\u200b", value=server_data[server]['modpack_description'], inline=False)
            info_embed.add_field(name="\u200b", value=server_data[server]['server_description'], inline=False)
            info_embed.add_field(name="\u200b", value=f"**Rules:** https://shadowraptor.net/rules/#{server_data[server]['address'].split('.')[0]}\n**Banned Items:** https://shadowraptor.net/banneditems/#{server_data[server]['address'].split('.')[0]}\n**Vote Links:** https://shadowraptor.net/voting/#{server_data[server]['address'].split('.')[0]}")
            info_embed.add_field(name="\u200b", value=f"The server is running;```v{server_data[server]['modpack_version']}```\n```Make sure to read all the information at the server spawn! It contains things you should not do, as well as helpful tips```", inline=False)

            message_embeds = [image_embed, info_embed]
            await interaction.response.send_message(embeds=message_embeds)

# Run the bot
raptor_bot.run(TOKEN)
