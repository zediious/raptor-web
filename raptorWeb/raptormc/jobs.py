from raptormc.views import player_poller
from os.path import join, getmtime
from logging import getLogger
from time import time
from json import dumps, load

from django.utils.html import strip_tags

from raptorWeb import settings
from raptormc.models import PlayerCount, PlayerName, Server

LOGGER = getLogger('raptormc.jobs')

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
        playerPoll()

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)

        export_server_data()
        playerPoll()
        
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
            with open(join(settings.BASE_DIR, 'server_announcements.json'), "r+") as announcement_json:
                announcement_dict = load(announcement_json)

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
                
                announcements = {}
                for server in server_data:
                    announcements.update({
                        server.server_address.split('.')[0]: {}
                    })
                for message in announcement_dict[key]:
                    announcements[key].update({
                        message: {
                            "author": announcement_dict[key][message]["author"],
                            "message": announcement_dict[key][message]["message"],
                            "date": announcement_dict[key][message]["date"]
                        }
                    })
  
                player_poller.currentPlayers_DB["server_info"].append({
                    f"server{server_number}": {
                        "key": key,
                        "state": player_data[key]["online"],
                        "maintenance": server_info.in_maintenance,
                        "address": server_info.server_address,
                        "names": PlayerName.objects.all().filter(server=Server.objects.get(server_address=player_data[key]["address"])),
                        "modpack_name": server_info.modpack_name,
                        "modpack_description": server_info.modpack_description,
                        "server_description": server_info.server_description,
                        "modpack": server_info.modpack_url,
                        "announcements": announcements,
                        "server_rules": server_info.server_rules,
                        "server_banned_items": server_info.server_banned_items,
                        "server_vote_links": server_info.server_vote_links
                    }
                })

                server_number += 1

            LOGGER.info("Request made, playerCounts.py ran")

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
                "modpack_description": strip_tags(server.modpack_description),
                "server_description": strip_tags(server.server_description),
                "modpack_url": server.modpack_url
            }
        })
        server_num += 1

    server_json = open(join(settings.BASE_DIR, 'server_data.json'), "w")
    server_json.write(dumps(current_servers, indent=4))
    server_json.close()
