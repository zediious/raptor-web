import discord
from json import dump, dumps, load
from json.decoder import JSONDecodeError
from time import time
import logging

from . import raptorbot_settings

async def get_server_roles(bot_instance):
    """
    Return role names and ids that match modpack names, keyed by their address key
    """
    server_data = dict(load(open('../../raptorWeb/server_data.json', "r")))
    sr_guild = bot_instance.get_guild(raptorbot_settings.DISCORD_GUILD)
    total_role_list = await sr_guild.fetch_roles()
    role_list = {}
    for server in server_data:
        for role in total_role_list:
            if role.name == str(f'{server_data[server]["modpack_name"]}'):
                role_list.update({
                    server_data[server]["address"].split('.')[0]: {
                        "id": role.id,
                        "name": role.name
                    }
                })
    return role_list

async def get_server_number(key):
    """
    Given a key, return the key for the upper dictionary a server is contained in
    """
    server_data = dict(load(open('../../raptorWeb/server_data.json', "r")))
    for server in server_data:
        if str(key) == server_data[server]["address"].split('.')[0]:
            return str(server)

async def update_global_announcements(bot_instance):
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    places their content in a Dictionary, nested in another
    dictionary keyed by a countered number. Data is saved
    to an "announcements.json" each iteration.
    """
    channel = bot_instance.get_channel(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID)
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

    announcementsJSON = open("../../raptorWeb/announcements.json", "w")
    announcementsJSON.write(dumps(announcements, indent=4))
    announcementsJSON.close()

async def update_all_server_announce(bot_instance):
    """
    Gets all messages from all server's selected channels, and adds any
    messages mentioning a server's role to a dictionary keyed  by the
    server. his is intended to be run once, if messages already existed
    in selected channels.
    """
    # Emptying file before running
    announcement_json = open("../../raptorWeb/server_announcements.json", "w")
    announcement_json.write('')
    announcement_json.close()

    server_data = dict(load(open('../../raptorWeb/server_data.json', "r")))
    for server in server_data:
        for channel in raptorbot_settings.SERVER_ANNOUNCEMENT_CHANNEL_IDS:
            if server_data[server]["address"].split('.')[0] == channel:
                await update_server_announce(server_key=server_data[server]["address"].split('.')[0], bot_instance=bot_instance)

async def update_server_announce(server_key, bot_instance):
    """
    Updates the announcement for a server passed as argument.
    Runs to update a server's messages when a message is sent 
    mentioning that server's role from it's selected channel.
    """
    server_num = await get_server_number(server_key)
    server_data = dict(load(open('../../raptorWeb/server_data.json', "r")))
    role_list = await get_server_roles(bot_instance=bot_instance)
    channel_instance = bot_instance.get_channel(raptorbot_settings.SERVER_ANNOUNCEMENT_CHANNEL_IDS[server_key])
    messages = [message async for message in channel_instance.history(limit=200)]
    announcements = None
    announcement_json = None

    try:
        announcement_json = open("../../raptorWeb/server_announcements.json", "r+")
        announcements = load(announcement_json)
    except JSONDecodeError as e:
        print(e)
        print("JSON does not exist. Will create")
        base_keys = {}
        for server in server_data:
            base_keys.update({
                server_data[server]["address"].split('.')[0]: {}
            })
        base_json = open("../../raptorWeb/server_announcements.json", "r+")
        dump(base_keys, base_json, indent=4)
        base_json.close()
        load_base_json = open("../../raptorWeb/server_announcements.json", "r+")
        announcements = load(load_base_json)
        load_base_json.close()
        
    for message in messages:
        current_time = time()
        if message.author != bot_instance.user:
            try:
                if message.author.get_role(raptorbot_settings.STAFF_ROLE_ID) != None:
                    if str(role_list[server_key]["id"]) in str(message.content):
                        try:
                            announcements[server_data[server_num]["address"].split('.')[0]].update({
                                f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
                                    "author": str(message.author),
                                    "message": message.content,
                                    "date": str(message.created_at.date().strftime('%B %d %Y'))
                                }
                            })
                        except KeyError as e:
                            print(f'An error occured attempting to find the "{e}" key within server_announcements.json. This should not happen!')
                            logging.critical(f'An error occured attempting to find the "{e}" key within server_announcements.json. This should not happen!')
            except AttributeError:
                continue

    finished_json = open("../../raptorWeb/server_announcements.json", "r+")
    dump(announcements, finished_json, indent=4)
    finished_json.close()

async def update_member_count(bot_instance):
    """
    Gets a count of total and online members on a
    provided Discord server, and places them in
    a dictionary. Data is saved to a "discordInfo.json"
    on each iteration.
    """
    server = bot_instance.get_guild(raptorbot_settings.DISCORD_GUILD)
    member_total = len(server.members)
    online_members = 0

    for member in server.members:

        if member.status != discord.Status.offline:
            online_members += 1

    discord_info = {
        "totalMembers": member_total,
        "onlineMembers": online_members
    }

    membersJSON = open("../../raptorWeb/discordInfo.json", "w")
    membersJSON.write(dumps(discord_info, indent=4))
    membersJSON.close()
