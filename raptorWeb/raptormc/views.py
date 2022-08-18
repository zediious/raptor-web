from django.shortcuts import render
from os.path import join, getmtime
from time import time
import logging

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.util import checkDatabase
from raptormc.models import PlayerCount, PlayerName, Server

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

player_poller = PlayerCounts()

class ShadowRaptor():

    LOGGER = logging.getLogger(__name__)

    NOMI = None
    NOMI_STATE = None
    E6E = None
    E6E_STATE = None
    CT2 = None
    CT2_STATE = None
    FTBUA = None
    FTBUA_STATE = None
    OB = None
    OB_STATE = None
    HEXXIT = None
    HEXXIT_STATE = None
    NETWORK = None

    PLAYER_STATS = []
    SERVER_STATES = []
    PLAYER_DATA = None
    SERVER_DATA = None

    class Info():

        def home_servers(request):
            
            playerPoll()
        
            PlayerCount.objects.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count'])
            PlayerName.objects.bulk_update(PlayerName.objects.all(), ['name'])
            Server.objects.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = player_poller.currentPlayers_DB)
        
        def rules(request):

            playerPoll()

            PlayerCount.objects.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count'])
            PlayerName.objects.bulk_update(PlayerName.objects.all(), ['name'])
            Server.objects.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context = player_poller.currentPlayers_DB)
            
        def banned_items(request):

            playerPoll()

            PlayerCount.objects.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count'])
            PlayerName.objects.bulk_update(PlayerName.objects.all(), ['name'])
            Server.objects.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context = player_poller.currentPlayers_DB)

def after_integrity():
    """
    Gets server and playercount objects from the database, only to be run
    after database integrity has been confirmed.
    """
    ShadowRaptor.NOMI = PlayerCount.objects.get(server=Server.objects.get(server_name="nomi"))
    ShadowRaptor.NOMI_STATE = Server.objects.get(server_name="nomi")
    ShadowRaptor.E6E = PlayerCount.objects.get(server=Server.objects.get(server_name="e6e"))
    ShadowRaptor.E6E_STATE = Server.objects.get(server_name="e6e")
    ShadowRaptor.CT2 = PlayerCount.objects.get(server=Server.objects.get(server_name="ct2"))
    ShadowRaptor.CT2_STATE = Server.objects.get(server_name="ct2")
    ShadowRaptor.FTBUA = PlayerCount.objects.get(server=Server.objects.get(server_name="ftbua"))
    ShadowRaptor.FTBUA_STATE = Server.objects.get(server_name="ftbua")
    ShadowRaptor.OB = PlayerCount.objects.get(server=Server.objects.get(server_name="ob"))
    ShadowRaptor.OB_STATE = Server.objects.get(server_name="ob")
    ShadowRaptor.HEXXIT = PlayerCount.objects.get(server=Server.objects.get(server_name="hexxit"))
    ShadowRaptor.HEXXIT_STATE = Server.objects.get(server_name="hexxit")
    ShadowRaptor.NETWORK = PlayerCount.objects.get(server=Server.objects.get(server_name="network"))

    ShadowRaptor.PLAYER_STATS = [ShadowRaptor.NOMI, ShadowRaptor.E6E, ShadowRaptor.CT2, ShadowRaptor.FTBUA, ShadowRaptor.OB, ShadowRaptor.HEXXIT, ShadowRaptor.NETWORK]
    ShadowRaptor.SERVER_STATES = [ShadowRaptor.NOMI_STATE, ShadowRaptor.E6E_STATE, ShadowRaptor.CT2_STATE, ShadowRaptor.FTBUA_STATE, ShadowRaptor.OB_STATE, ShadowRaptor.HEXXIT_STATE]

def playerPoll():
    """
    Request Player data From MCAPI and make
    changes to the database. Will only run if created
    .LOCK file hasn't been written to in 2 minutes. Will confirm
    that database objects are created, before getting them.
    """
    try:

        lock_time = time() - getmtime(join(settings.BASE_DIR, 'playerCounts.LOCK'))

        if  lock_time >= 120:
            
            player_data = player_poller.get_current_players()

            checkDatabase.confirm_database_integrity()

            after_integrity()

            ShadowRaptor.NETWORK.player_count = player_data["totalCount"]
            ShadowRaptor.NOMI.player_count = player_data["nomi"]["count"]
            ShadowRaptor.NOMI_STATE.server_state = player_data["nomi"]["online"]
            ShadowRaptor.E6E.player_count = player_data["e6e"]["count"]
            ShadowRaptor.E6E_STATE.server_state = player_data["e6e"]["online"]
            ShadowRaptor.CT2.player_count = player_data["ct2"]["count"]
            ShadowRaptor.CT2_STATE.server_state = player_data["ct2"]["online"]
            ShadowRaptor.FTBUA.player_count = player_data["ftbu"]["count"]
            ShadowRaptor.FTBUA_STATE.server_state = player_data["ftbu"]["online"]
            ShadowRaptor.OB.player_count = player_data["ob"]["count"]
            ShadowRaptor.OB_STATE.server_state = player_data["ob"]["online"]

            PlayerName.objects.all().delete()

            totalCount = str(ShadowRaptor.NETWORK.player_count)
            
            for player in player_data["nomi"]["names"]:

                PlayerName.objects.create(server=Server.objects.get(server_name="nomi") , name=player)
            
            for player in player_data["e6e"]["names"]:

                PlayerName.objects.create(server=Server.objects.get(server_name="e6e") , name=player)

            for player in player_data["ct2"]["names"]:

                PlayerName.objects.create(server=Server.objects.get(server_name="ct2") , name=player)

            for player in player_data["ftbu"]["names"]:

                PlayerName.objects.create(server=Server.objects.get(server_name="ftbua"), name=player)

            for player in player_data["ob"]["names"]:

                PlayerName.objects.create(server=Server.objects.get(server_name="ob") , name=player)

            player_names = PlayerName.objects.all()
            
            player_poller.currentPlayers_DB = {"player_count": totalCount,
                                            "nomi_names": player_names.filter(server=Server.objects.get(server_name="nomi")),
                                            "nomi_state": ShadowRaptor.NOMI_STATE.server_state,
                                            "e6e_names": player_names.filter(server=Server.objects.get(server_name="e6e")),
                                            "e6e_state": ShadowRaptor.E6E_STATE.server_state,
                                            "ct2_names": player_names.filter(server=Server.objects.get(server_name="ct2")),
                                            "ct2_state": ShadowRaptor.CT2_STATE.server_state,
                                            "ftbu_names": player_names.filter(server=Server.objects.get(server_name="ftbua")),
                                            "ftbu_state": ShadowRaptor.FTBUA_STATE.server_state,
                                            "ob_names": player_names.filter(server=Server.objects.get(server_name="ob")),
                                            "ob_state": ShadowRaptor.OB_STATE.server_state,
                                            "hexxit_names": "not implemented"}

            ShadowRaptor.LOGGER.error("[INFO] Request made, playerCounts.py ran")

        else:

            ShadowRaptor.LOGGER.error("[INFO] Request made, not enough time has passed to run playerCounts.py")

    except FileNotFoundError as e:

        ShadowRaptor.LOGGER.error(e)
        ShadowRaptor.LOGGER.error("[ERROR] playerCounts.LOCK file not present. Please create the file at the above path.")
