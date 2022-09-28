from raptormc.views import player_poller
from os.path import join, getmtime
from logging import getLogger
from time import time

from django.utils import timezone

from raptorWeb import settings
from raptormc.util import checkDatabase
from raptormc.models import PlayerCount, PlayerName, Server, ServerInformation

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

            PlayerCount.objects.create(server=Server.objects.get(server_name="network"), player_count=player_data["totalCount"]).save()

            for key in player_data:

                if key == "totalCount":

                    continue

                for player in player_data[key]["names"]:

                    PlayerName.objects.create(server=Server.objects.get(server_name=key) , name=player).save()

                PlayerCount.objects.create(server=Server.objects.get(server_name=key), player_count=player_data[key]["count"]).save()

            totalCount = PlayerCount.objects.get(server=Server.objects.get(server_name="network")).player_count
            player_names = PlayerName.objects.all()
            nomi_info = ServerInformation.objects.get(server=Server.objects.get(server_name="nomi"))
            e6e_info = ServerInformation.objects.get(server=Server.objects.get(server_name="e6e"))
            ct2_info = ServerInformation.objects.get(server=Server.objects.get(server_name="ct2"))
            ftbu_info = ServerInformation.objects.get(server=Server.objects.get(server_name="ftbu"))
            ob_info = ServerInformation.objects.get(server=Server.objects.get(server_name="ob"))
            atm7_info = ServerInformation.objects.get(server=Server.objects.get(server_name="atm7"))
            
            player_poller.currentPlayers_DB = {"player_count": totalCount,
                                            "nomi_names": player_names.filter(server=Server.objects.get(server_name="nomi")),
                                            "nomi_state": player_data["nomi"]["online"],
                                            "nomi_maintenance": nomi_info.in_maintenance,
                                            "nomi_info": {
                                                "address": nomi_info.server_address,
                                                "modpack_description": nomi_info.modpack_description,
                                                "server_description": nomi_info.server_description,
                                                "modpack": nomi_info.modpack_url,
                                                "server_rules": nomi_info.server_rules,
                                                "server_banned_items": nomi_info.server_banned_items,
                                                "server_vote_links": nomi_info.server_vote_links
                                            },
                                            "e6e_names": player_names.filter(server=Server.objects.get(server_name="e6e")),
                                            "e6e_state": player_data["e6e"]["online"],
                                            "e6e_maintenance": e6e_info.in_maintenance,
                                            "e6e_info": {
                                                "address": e6e_info.server_address,
                                                "modpack_description": e6e_info.modpack_description,
                                                "server_description": e6e_info.server_description,
                                                "modpack": e6e_info.modpack_url,
                                                "server_rules": e6e_info.server_rules,
                                                "server_banned_items": e6e_info.server_banned_items,
                                                "server_vote_links": e6e_info.server_vote_links
                                            },
                                            "ct2_names": player_names.filter(server=Server.objects.get(server_name="ct2")),
                                            "ct2_state": player_data["ct2"]["online"],
                                            "ct2_maintenance": ct2_info.in_maintenance,
                                            "ct2_info": {
                                                "address": ct2_info.server_address,
                                                "modpack_description": ct2_info.modpack_description,
                                                "server_description": ct2_info.server_description,
                                                "modpack": ct2_info.modpack_url,
                                                "server_rules": ct2_info.server_rules,
                                                "server_banned_items": ct2_info.server_banned_items,
                                                "server_vote_links": ct2_info.server_vote_links
                                            },
                                            "ftbu_names": player_names.filter(server=Server.objects.get(server_name="ftbu")),
                                            "ftbu_state": player_data["ftbu"]["online"],
                                            "ftbu_maintenance": ftbu_info.in_maintenance,
                                            "ftbu_info": {
                                                "address": ftbu_info.server_address,
                                                "modpack_description": ftbu_info.modpack_description,
                                                "server_description": ftbu_info.server_description,
                                                "modpack": ftbu_info.modpack_url,
                                                "server_rules": ftbu_info.server_rules,
                                                "server_banned_items": ftbu_info.server_banned_items,
                                                "server_vote_links": ftbu_info.server_vote_links
                                            },
                                            "ob_names": player_names.filter(server=Server.objects.get(server_name="ob")),
                                            "ob_state": player_data["ob"]["online"],
                                            "ob_maintenance": ob_info.in_maintenance,
                                            "ob_info": {
                                                "address": ob_info.server_address,
                                                "modpack_description": ob_info.modpack_description,
                                                "server_description": ob_info.server_description,
                                                "modpack": ob_info.modpack_url,
                                                "server_rules": ob_info.server_rules,
                                                "server_banned_items": ob_info.server_banned_items,
                                                "server_vote_links": ob_info.server_vote_links
                                            },
                                            "atm7_names": player_names.filter(server=Server.objects.get(server_name="atm7")),
                                            "atm7_state": player_data["atm7"]["online"],
                                            "atm7_maintenance": atm7_info.in_maintenance,
                                            "atm7_info": {
                                                "address": atm7_info.server_address,
                                                "modpack_description": atm7_info.modpack_description,
                                                "server_description": atm7_info.server_description,
                                                "modpack": atm7_info.modpack_url,
                                                "server_rules": atm7_info.server_rules,
                                                "server_banned_items": atm7_info.server_banned_items,
                                                "server_vote_links": atm7_info.server_vote_links
                                            }}

            LOGGER.error("[INFO][{}] Request made, playerCounts.py ran".format(timezone.now().isoformat()))

        else:

            LOGGER.error("[INFO][{}] Request made, not enough time has passed to run playerCounts.py".format(timezone.now().isoformat()))

    except FileNotFoundError as e:

        LOGGER.error(e)
        LOGGER.error("[ERROR][{}] playerCounts.LOCK file not present. Please create the file at the above path.".format(timezone.now().isoformat()))
