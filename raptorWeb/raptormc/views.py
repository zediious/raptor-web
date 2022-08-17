import asyncio
from django.shortcuts import render
from os.path import join, getmtime
from time import sleep, time
import logging

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.models import PlayerData, Server

# Create your views here.

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

player_poller = PlayerCounts()

loop = asyncio.get_event_loop()

class ShadowRaptor():

    LOGGER = logging.getLogger(__name__)
    
    NOMI = PlayerData.objects.get(pk=1)
    NOMI_STATE = Server.objects.get(pk=1)
    E6E = PlayerData.objects.get(pk=2)
    E6E_STATE = Server.objects.get(pk=2)
    CT2 = PlayerData.objects.get(pk=3)
    CT2_STATE = Server.objects.get(pk=3)
    FTBUA = PlayerData.objects.get(pk=4)
    FTBUA_STATE = Server.objects.get(pk=4)
    OB = PlayerData.objects.get(pk=5)
    OB_STATE = Server.objects.get(pk=5)
    HEXXIT = PlayerData.objects.get(pk=6)
    HEXXIT_STATE = Server.objects.get(pk=6)
    NETWORK = PlayerData.objects.get(pk=7)

    PLAYER_STATS = [NOMI, E6E, CT2, FTBUA, OB, HEXXIT, NETWORK]

    SERVER_STATES = [NOMI_STATE, E6E_STATE, CT2_STATE, FTBUA_STATE, OB_STATE, HEXXIT_STATE]

    PLAYER_DATA = PlayerData.objects

    SERVER_DATA = Server.objects

    class Info():

        def home_servers(request):

            task = loop.create_task(playerPoll())
            loop.run_until_complete(task)
        
            ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count', 'player_names'])
            ShadowRaptor.SERVER_DATA.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = player_poller.currentPlayers_DB)
        
        def rules(request):

            task = loop.create_task(playerPoll())
            loop.run_until_complete(task)

            ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count', 'player_names'])
            ShadowRaptor.SERVER_DATA.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context = player_poller.currentPlayers_DB)
            
        def banned_items(request):

            task = loop.create_task(playerPoll())
            loop.run_until_complete(task)

            ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.PLAYER_STATS, ['player_count', 'player_names'])
            ShadowRaptor.SERVER_DATA.bulk_update(ShadowRaptor.SERVER_STATES, ['server_state'])

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context = player_poller.currentPlayers_DB)

async def playerPoll():
    """
    Asynchronously request Player data From MCAPI and make
    changes to the database. Will only run if created
    .LOCK file hasn't been written to in 2 minutes
    """
    try:

        lock_time = time() - getmtime(join(settings.BASE_DIR, 'playerCounts.LOCK'))

        if  lock_time >= 120:
        
            player_data = player_poller.get_current_players()

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

            ShadowRaptor.LOGGER.error("playerCounts.py ran")

        else:

            ShadowRaptor.LOGGER.error("Not enough time has passed to run playerCounts.py")

    except FileNotFoundError as e:

        ShadowRaptor.LOGGER.error(e)
        ShadowRaptor.LOGGER.error("[ERROR] playerCounts.LOCK file not present. Please create the file at the above path.")
