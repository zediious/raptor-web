from raptormc.views import player_poller
from os.path import join, getmtime
from logging import getLogger
from time import time

from django.utils import timezone

from raptorWeb import settings
from raptormc.models import PlayerCount, PlayerName, Server

LOGGER = getLogger(__name__)

class RaptorWare:
    """
    Middleware containing code to run on first initilization, as well as code to
    run whenever a request is made, before the view is displayed.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        playerPoll()

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)

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

        if  lock_time >= 10:

            server_data = Server.objects.all()

            server_key = 0
            for server in server_data:

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
                        "server_rules": server_info.server_rules,
                        "server_banned_items": server_info.server_banned_items,
                        "server_vote_links": server_info.server_vote_links
                    }
                })

                server_number += 1

            LOGGER.error("[INFO][{}] Request made, playerCounts.py ran".format(timezone.now().isoformat()))

        else:

            LOGGER.error("[INFO][{}] Request made, not enough time has passed to run playerCounts.py".format(timezone.now().isoformat()))

    except FileNotFoundError as e:

        LOGGER.error(e)
        LOGGER.error("[ERROR][{}] playerCounts.LOCK file not present. Please create the file at the above path.".format(timezone.now().isoformat()))
