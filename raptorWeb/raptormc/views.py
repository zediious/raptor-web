from django.shortcuts import render
from os.path import join, getmtime
from time import time
import logging

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.util import checkDatabase
from raptormc.models import PlayerData, Server
# Create your views here.

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
        
            PlayerData.objects.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count', 'player_names'])
            Server.objects.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = player_poller.currentPlayers_DB)
        
        def rules(request):

            playerPoll()

            PlayerData.objects.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count', 'player_names'])
            Server.objects.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context = player_poller.currentPlayers_DB)
            
        def banned_items(request):

            playerPoll()

            PlayerData.objects.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count', 'player_names'])
            Server.objects.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context = player_poller.currentPlayers_DB)

def after_integrity():
    """
    Gets server and playerdata objects from the database, only to be run
    after database integrity has been confirmed.
    """
    ShadowRaptor.NOMI = PlayerData.objects.get(pk=1)
    ShadowRaptor.NOMI_STATE = Server.objects.get(server_name="nomi")
    ShadowRaptor.E6E = PlayerData.objects.get(pk=2)
    ShadowRaptor.E6E_STATE = Server.objects.get(pk=2)
    ShadowRaptor.CT2 = PlayerData.objects.get(pk=3)
    ShadowRaptor.CT2_STATE = Server.objects.get(pk=3)
    ShadowRaptor.FTBUA = PlayerData.objects.get(pk=4)
    ShadowRaptor.FTBUA_STATE = Server.objects.get(pk=4)
    ShadowRaptor.OB = PlayerData.objects.get(pk=5)
    ShadowRaptor.OB_STATE = Server.objects.get(pk=5)
    ShadowRaptor.HEXXIT = PlayerData.objects.get(pk=6)
    ShadowRaptor.HEXXIT_STATE = Server.objects.get(pk=6)
    ShadowRaptor.NETWORK = PlayerData.objects.get(pk=7)

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
            ShadowRaptor.NOMI.player_names = player_data["nomi"]["names"]
            ShadowRaptor.NOMI_STATE.server_state = player_data["nomi"]["online"]
            ShadowRaptor.E6E.player_count = player_data["e6e"]["count"]
            ShadowRaptor.E6E.player_names = player_data["e6e"]["names"]
            ShadowRaptor.E6E_STATE.server_state = player_data["e6e"]["online"]
            ShadowRaptor.CT2.player_count = player_data["ct2"]["count"]
            ShadowRaptor.CT2.player_names = player_data["ct2"]["names"]
            ShadowRaptor.CT2_STATE.server_state = player_data["ct2"]["online"]
            ShadowRaptor.FTBUA.player_count = player_data["ftbu"]["count"]
            ShadowRaptor.FTBUA.player_names = player_data["ftbu"]["names"]
            ShadowRaptor.FTBUA_STATE.server_state = player_data["ftbu"]["online"]
            ShadowRaptor.OB.player_count = player_data["ob"]["count"]
            ShadowRaptor.OB.player_names = player_data["ob"]["names"]
            ShadowRaptor.OB_STATE.server_state = player_data["ob"]["online"]

            totalCount = str(ShadowRaptor.NETWORK)[0]
            nomiNames = str(ShadowRaptor.NOMI)[3:].replace('[','').replace(']','')
            e6eNames = str(ShadowRaptor.E6E)[3:].replace('[','').replace(']','')
            ct2Names = str(ShadowRaptor.CT2)[3:].replace('[','').replace(']','')
            ftbuNames = str(ShadowRaptor.FTBUA)[3:].replace('[','').replace(']','')
            obNames = str(ShadowRaptor.OB)[3:].replace('[','').replace(']','')
            hexxitNames = str(ShadowRaptor.HEXXIT)[3:].replace('[','').replace(']','')

            player_poller.currentPlayers_DB = {"player_count": totalCount,
                                            "nomi_names": nomiNames,
                                            "nomi_state": ShadowRaptor.NOMI_STATE.server_state,
                                            "e6e_names": e6eNames,
                                            "e6e_state": ShadowRaptor.E6E_STATE.server_state,
                                            "ct2_names": ct2Names,
                                            "ct2_state": ShadowRaptor.CT2_STATE.server_state,
                                            "ftbu_names": ftbuNames,
                                            "ftbu_state": ShadowRaptor.FTBUA_STATE.server_state,
                                            "ob_names": obNames,
                                            "ob_state": ShadowRaptor.OB_STATE.server_state,
                                            "hexxit_names": hexxitNames}

            ShadowRaptor.LOGGER.error("[INFO] Request made, playerCounts.py ran")

        else:

            ShadowRaptor.LOGGER.error("[INFO] Request made, not enough time has passed to run playerCounts.py")

    except FileNotFoundError as e:

        ShadowRaptor.LOGGER.error(e)
        ShadowRaptor.LOGGER.error("[ERROR] playerCounts.LOCK file not present. Please create the file at the above path.")
