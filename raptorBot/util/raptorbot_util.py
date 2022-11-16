import discord
from json import dump, dumps, load
from time import time

import raptorbot_settings
from ..bot import raptor_bot

async def get_server_roles():
    """
    Return role names and ids that match modpack names, keyed by their address key
    """
    server_data = dict(load(open('../raptorWeb/server_data.json', "r")))
    sr_guild = raptor_bot.get_guild(raptorbot_settings.DISCORD_GUILD)
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

async def update_global_announcements():
    """
    Gets all messages from defined "ANNOUNCEMENT_CHANNEL" and
    places their content in a Dictionary, nested in another
    dictionary keyed by a countered number. Data is saved
    to an "announcements.json" each iteration.
    """
    channel = raptor_bot.get_channel(raptorbot_settings.ANNOUNCEMENT_CHANNEL_ID)
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

async def update_all_server_announce():
    """
    Gets all messages from all server's selected channels, and adds any
    messages mentioning a server's role to a dictionary keyed  by the
    server. his is intended to be run once, if messages already existed
    in selected channels.
    """
    server_data = dict(load(open('../raptorWeb/server_data.json', "r")))
    for server in server_data:
        update_server_announce(server_data[server]["address"].split('.')[0])

async def update_server_announce(server_key):
    """
    Updates the announcement for a server passed as argument.
    Runs to update a server's messages when a message is sent 
    mentioning that server's role from it's selected channel.
    """
    server_data = dict(load(open('../raptorWeb/server_data.json', "r")))
    channel_instance = raptor_bot.get_channel(raptorbot_settings.SERVER_ANNOUNCEMENT_CHANNEL_IDS[server_key])
    messages = [message async for message in channel_instance.history(limit=200)]
    announcements = {}
    for message in messages:
        current_time = time()
        try:
            announcements[server_data[server_key]["address"].split('.')[0]].update({
                f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
                    "author": str(message.author),
                    "message": message.content,
                    "date": str(message.created_at.date().strftime('%B %d %Y'))
                }
            })
        # If a dictionary keyed by server role/modpack name doesn't exist, create it first.
        except KeyError as e:
            announcements.update({
                server_data[server_key]["address"].split('.')[0]: {}
            })
            announcements[server_data[server_key]["address"].split('.')[0]].update({
                f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
                    "author": str(message.author),
                    "message": message.content,
                    "date": str(message.created_at.date().strftime('%B %d %Y'))
                }
            })
    with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
        dump(announcements, announcement_json, indent=4)

# async def add_server_announcement(message):
#     """
#     If a message was sent mentioning a Server's role, the message along 
#     with it's author and date will be added to a dictionary keyed 
#     by the server
#     """
#     if message.author != raptor_bot.user:
#         if message.author.get_role(STAFF_ROLE_ID) != None:
#             try:
#                 lock_time = time() - getmtime('update_server_announcements.LOCK')
            
#                 if lock_time >= 10: 
#                     announcement_dict = {}
#                     try:
#                         with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
#                             announcement_dict = load(announcement_json)
#                     except:
#                         with open("../raptorWeb/server_announcements.json", "w") as create_file:
#                             create_file.write('{}')
#                             print('Created empty server_announcements.json')
#                         with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
#                             announcement_dict = load(announcement_json)
#                     with open("../raptorWeb/server_announcements.json", "r+") as announcement_json:
#                         server_data = dict(load(open('../raptorWeb/server_data.json', "r")))
#                         sr_guild = raptor_bot.get_guild(DISCORD_GUILD)
#                         announcement_json.seek(0)
#                         role_list = get_server_roles()
#                         # Check if message contains a mention of roles found above, if a match is found it is saved
#                         for server in server_data:
#                             for role in role_list:
#                                 if str(role_list[role]["id"]) in str(message.content) and str(role_list[role]["name"]) == server_data[server]["modpack_name"]:
#                                     current_time = time()
#                                     try:
#                                         announcement_dict[server_data[server]["address"].split('.')[0]].update({
#                                             f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
#                                                 "author": str(message.author),
#                                                 "message": message.content,
#                                                 "date": str(message.created_at.date().strftime('%B %d %Y'))
#                                             }
#                                         })
#                                     # If a dictionary keyed by server role/modpack name doesn't exist, create it first.
#                                     except KeyError as e:
#                                         announcement_dict.update({
#                                             server_data[server]["address"].split('.')[0]: {}
#                                         })
#                                         announcement_dict[server_data[server]["address"].split('.')[0]].update({
#                                             f"message_{str(message.author)}-{str(message.created_at.date().strftime(f'{current_time}-%B-%d-%Y'))}": {
#                                                 "author": str(message.author),
#                                                 "message": message.content,
#                                                 "date": str(message.created_at.date().strftime('%B %d %Y'))
#                                             }
#                                         })


#                         dump(announcement_dict, announcement_json, indent=4)

#                     with open('update_server_announcements.LOCK', 'w') as lock_file:
#                         lock_file.write("update_server_announcements function LOCK File. Do not modify manually.")

#                 else:
#                     print("Not enough time has passed to update server announcements")

#             except FileNotFoundError as e:
#                 print(f"{e}\n")
#                 print("update_server_announcements.LOCK file not found. Create a file with this exact name in the same directory as bot.py.")


async def update_member_count():
    """
    Gets a count of total and online members on a
    provided Discord server, and places them in
    a dictionary. Data is saved to a "discordInfo.json"
    on each iteration.
    """
    server = raptor_bot.get_guild(raptorbot_settings.DISCORD_GUILD)
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
