from os.path import join, getmtime
from logging import getLogger
from time import time
from json import dumps, load

from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.timezone import localtime, now

import requests
from shutil import copyfile

from raptorWeb import settings
from raptormc.models import PlayerCount, PlayerName, Server, User, UserProfileInfo, DiscordUserInfo
from raptormc.util.playerCounts import PlayerCounts

LOGGER = getLogger('raptormc.jobs')
player_poller = PlayerCounts()

class RaptorWare:
    """
    Middleware containing code to run on first initilization, as well as code to
    run whenever a request is made, before the view is displayed.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        export_server_data()

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)

        export_server_data()
        
        return response

def playerPoll():
    """
    Query addresses provided in all Server objects and add PlayerName and 
    PlayerCount objects to the database with a foreign key for each Server. 
    Will only run if created .LOCK file hasn't been written to in 2 minutes.
    """
    try:

        lock_time = time() - getmtime(join(settings.BASE_DIR, 'playerCounts.LOCK'))

        if  settings.ENABLE_SERVER_QUERY and lock_time >= 120 and Server.objects.count() > 0:

            server_data = Server.objects.all()

            server_key = 0
            for server in server_data:

                if server.server_address == "Default":
                    LOGGER.error("A server(s) exist, however they still have the default address set.")
                    break
                
                player_poller.server_data.update({
                    f"server{server_key}": {
                        "address": server.server_address,
                        "port": server.server_port
                    }
                })

                server_key += 1
            
            player_data = player_poller.get_current_players()

            PlayerCount.objects.all().delete()
            PlayerName.objects.all().delete()

            announcement_dict = {}
            do_announcement = False
            try:
                with open(join(settings.BASE_DIR, 'server_announcements.json'), "r+") as announcement_json:
                    announcement_dict = load(announcement_json)
                    if announcement_dict != {}:
                        do_announcement = True
            except Exception as e:
                LOGGER.info('server_announcements.json not present, allow Discord Bot to create and populate this file')
                do_announcement = False

            player_poller.currentPlayers_DB.update({
                "totalCount": player_data["totalCount"]
            })
            
            player_poller.currentPlayers_DB["server_info"] = []
            server_number = 0
            for key in player_data:

                if key == "totalCount":

                    continue

                for player in player_data[key]["names"]:

                    PlayerName.objects.create(server=Server.objects.get(server_address=player_data[key]["address"]), name=player).save()

                PlayerCount.objects.create(server=Server.objects.get(server_address=player_data[key]["address"]), player_count=player_data[key]["count"]).save()

                server_info = Server.objects.get(server_address=player_data[key]["address"])
                
                announcements = []
                if do_announcement == True:

                    try:
                        for message in announcement_dict[key]:
                            announcements.append({
                                message: {
                                    "author": announcement_dict[key][message]["author"],
                                    "message": announcement_dict[key][message]["message"],
                                    "date": announcement_dict[key][message]["date"]
                                }
                            })
                    except KeyError as e:
                        LOGGER.info("A Server exists, however no announcements have been made regarding it yet. Skipping.")
  
                player_poller.currentPlayers_DB["server_info"].append({
                    f"server{server_number}": {
                        "key": key,
                        "state": player_data[key]["online"],
                        "maintenance": server_info.in_maintenance,
                        "player_count": player_data[key]["count"],
                        "address": server_info.server_address,
                        "names": PlayerName.objects.all().filter(server=Server.objects.get(server_address=player_data[key]["address"])),
                        "modpack_name": server_info.modpack_name,
                        "modpack_version": server_info.modpack_version,
                        "modpack_description": server_info.modpack_description,
                        "server_description": server_info.server_description,
                        "modpack": server_info.modpack_url,
                        "announcements": announcements,
                        "announcement_count": len(announcements),
                        "server_rules": server_info.server_rules,
                        "server_banned_items": server_info.server_banned_items,
                        "server_vote_links": server_info.server_vote_links
                    }
                })

                server_number += 1

            LOGGER.info("Request made, playerCounts.py ran")

            # All user profile picture URLs to context
            all_normal_users = User.objects.all()
            all_discord_users = DiscordUserInfo.objects.all()
            player_poller.currentPlayers_DB.update({
                "users": []
            })
            for user in all_normal_users:
                try: 
                    user_core = UserProfileInfo.objects.get(user=user)
                except UserProfileInfo.DoesNotExist:
                    continue
                if settings.DEBUG:
                    player_poller.currentPlayers_DB["users"].append({
            
                        "username": user.username,
                        "profile_picture": f'http://{settings.DOMAIN_NAME}/media/{user_core.profile_picture.name}'
                        
                    })
                else:
                    player_poller.currentPlayers_DB["users"].append({
            
                        "username": user.username,
                        "profile_picture": f'https://{settings.DOMAIN_NAME}/media/{user_core.profile_picture.name}'
                        
                    })
            for user in all_discord_users:
                player_poller.currentPlayers_DB["users"].append({
                    
                    "username": user.username,
                    "profile_picture": user.profile_picture
                    
                })

            # Settings to context
            player_poller.currentPlayers_DB.update({
                "pub_domain": settings.DOMAIN_NAME,
                "default_media": f'http://{settings.DOMAIN_NAME}/media/'
            })

        else:

            LOGGER.info("Request made, not enough time has passed to run playerCounts.py")

    except FileNotFoundError as e:

        LOGGER.error(e)
        LOGGER.error("playerCounts.LOCK file not present. Please create the file at the above path.")

def export_server_data():
    """
    Export current Server Models to a json file
    """
    current_servers = {}
    server_num = 0

    for server in Server.objects.all():

        current_servers.update({
            f'server{server_num}': {
                "address": server.server_address,
                "modpack_name": server.modpack_name,
                "modpack_version": server.modpack_version,
                "modpack_description": strip_tags(server.modpack_description).replace('&gt;', '>').replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'"),
                "server_description": strip_tags(server.server_description).replace('&gt;', '>').replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'"),
                "modpack_url": server.modpack_url
            }
        })
        server_num += 1

    server_json = open(join(settings.BASE_DIR, 'server_data.json'), "w")
    server_json.write(dumps(current_servers, indent=4))
    server_json.close()
  
def export_users():
    normal_user_into_raptoruser = {}
    discord_user_into_raptoruser = {}
    normal_user_list = UserProfileInfo.objects.all()
    for user in normal_user_list:
        normal_user_into_raptoruser.update({
            f'{user.user.username}': {
                "username": user.user.username,
                "user_slug": slugify(user.user.username),
                "email": user.user.email,
                "date_joined": str(localtime(now())),
                "last_login": str(localtime(now())),
                "password": user.user.password,
                "user_profile_info": {
                    "picture_has_been_changed": True,
                    "minecraft_username": user.minecraft_username,
                    "favorite_modpack": user.favorite_modpack
                }
            }
        })
    normal_user_list_json = open(join(settings.BASE_DIR, 'normal_user_list.json'), "w")
    normal_user_list_json.write(dumps(normal_user_into_raptoruser, indent=4))
    normal_user_list_json.close()
    discord_user_list = DiscordUserInfo.objects.all()
    for user in discord_user_list:
        discord_user_into_raptoruser.update({
            f'{user.username}': {
                "username": user.username,
                "user_slug": slugify(user.username),
                "date_joined": str(localtime(now())),
                "last_login": str(localtime(now())),
                "user_profile_info": {
                    "picture_has_been_changed": True,
                    "minecraft_username": user.minecraft_username,
                    "favorite_modpack": user.favorite_modpack
                },
                "discord_user_info": {
                    "id": user.id,
                    "tag": user.tag,
                    "pub_flags": user.pub_flags,
                    "flags": user.flags,
                    "locale": user.locale,
                    "mfa_enabled": user.mfa_enabled
                }
            }
        })
    discord_user_list_json = open(join(settings.BASE_DIR, 'discord_user_list.json'), "w")
    discord_user_list_json.write(dumps(discord_user_into_raptoruser, indent=4))
    discord_user_list_json.close()
