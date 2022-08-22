from raptormc.views import player_poller
from os.path import join, getmtime
from logging import getLogger
from time import time

from raptorWeb import settings
from raptormc.util import checkDatabase
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
        save_models()

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)

        playerPoll()
        save_models()
        
        return response

def playerPoll():
    """
    Query ShadowRaptor servers and add PlayerName and PlayerCount
    objects to the database with a foreign key for each server. Will 
    only run if created .LOCK file hasn't been written to in 2 minutes. 
    Will confirm that Server objects exist, before getting them.
    """
    try:

        lock_time = time() - getmtime(join(settings.BASE_DIR, 'playerCounts.LOCK'))

        if  lock_time >= 120:
            
            player_data = player_poller.get_current_players()

            checkDatabase.confirm_database_integrity()

            PlayerCount.objects.all().delete()
            PlayerName.objects.all().delete()

            PlayerCount.objects.create(server=Server.objects.get(server_name="network"), player_count=player_data["totalCount"])

            for key in player_data:

                if key == "totalCount":

                    continue

                for player in player_data[key]["names"]:

                    PlayerName.objects.create(server=Server.objects.get(server_name=key) , name=player)

                PlayerCount.objects.create(server=Server.objects.get(server_name=key), player_count=player_data[key]["count"])

            totalCount = PlayerCount.objects.get(server=Server.objects.get(server_name="network")).player_count
            player_names = PlayerName.objects.all()
            
            player_poller.currentPlayers_DB = {"player_count": totalCount,
                                            "nomi_names": player_names.filter(server=Server.objects.get(server_name="nomi")),
                                            "nomi_state": player_data["nomi"]["online"],
                                            "e6e_names": player_names.filter(server=Server.objects.get(server_name="e6e")),
                                            "e6e_state": player_data["e6e"]["online"],
                                            "ct2_names": player_names.filter(server=Server.objects.get(server_name="ct2")),
                                            "ct2_state": player_data["ct2"]["online"],
                                            "ftbu_names": player_names.filter(server=Server.objects.get(server_name="ftbu")),
                                            "ftbu_state": player_data["ftbu"]["online"],
                                            "ob_names": player_names.filter(server=Server.objects.get(server_name="ob")),
                                            "ob_state": player_data["ob"]["online"],
                                            "hexxit_names": "not implemented",
                                            "hexxit_state": False}

            LOGGER.error("[INFO] Request made, playerCounts.py ran")

        else:

            LOGGER.error("[INFO] Request made, not enough time has passed to run playerCounts.py")

    except FileNotFoundError as e:

        LOGGER.error(e)
        LOGGER.error("[ERROR] playerCounts.LOCK file not present. Please create the file at the above path.")

def save_models():
    """
    Bulk update PlayerCount, PlayerName, and Server objects, specifically
    attributes from them that were modified while running playerPoll().
    """
    PlayerCount.objects.bulk_update(PlayerCount.objects.all(), ['player_count'])
    PlayerName.objects.bulk_update(PlayerName.objects.all(), ['name'])
    Server.objects.bulk_update(Server.objects.all(), ['server_state'])
