import asyncio
from turtle import home, update
from django.shortcuts import render
from asgiref.sync import sync_to_async
from os.path import join
import logging

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.models import PlayerData

# Create your views here.

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

class ShadowRaptor():

    LOGGER = logging.getLogger(__name__)
    
    NOMI = PlayerData.objects.get(pk=1)
    E6E = PlayerData.objects.get(pk=2)
    CT2 = PlayerData.objects.get(pk=3)
    FTBUA = PlayerData.objects.get(pk=4)
    OB = PlayerData.objects.get(pk=5)
    HEXXIT = PlayerData.objects.get(pk=6)
    NETWORK = PlayerData.objects.get(pk=7)

    SERVERS = [NOMI, E6E, CT2, FTBUA, OB, HEXXIT, NETWORK]

    PLAYER_DATA = PlayerData.objects

    class Info():

        def home_servers(request):

            home_servers_data = updateData(buffer())
            
            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = home_servers_data)
        
        def rules(request):

            home_servers_data = updateData(buffer())

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context= home_servers_data)
            
        def banned_items(request):

            home_servers_data = updateData(buffer())

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context= home_servers_data)

# def update():
#     """
#     MCAPI request and database updates encapsulated in async coroutine
#     """
#     player_poller = PlayerCounts()
#     player_data = player_poller.get_current_players()

#     ShadowRaptor.NETWORK.player_count = player_data.get_total_count()
#     ShadowRaptor.NOMI.player_count = player_data["nomi"]["count"]
#     ShadowRaptor.NOMI.player_names = player_data["nomi"]["names"]
#     ShadowRaptor.E6E.player_count = player_data["e6e"]["count"]
#     ShadowRaptor.E6E.player_names = player_data["e6e"]["names"]
#     ShadowRaptor.CT2.player_count = player_data["ct2"]["count"]
#     ShadowRaptor.CT2.player_names = player_data["ct2"]["names"]
#     ShadowRaptor.FTBUA.player_count = player_data["ftbu"]["count"]
#     ShadowRaptor.FTBUA.player_names = player_data["ftbu"]["names"]
#     ShadowRaptor.OB.player_count = player_data["ob"]["count"]
    
#     ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.SERVERS, ['player_count'])
#     ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.SERVERS, ['player_names'])

#     totalCount = str(ShadowRaptor.NETWORK)[0]
#     nomiNames = str(ShadowRaptor.NOMI)[3:].replace('[','').replace(']','')
#     e6eNames = str(ShadowRaptor.E6E)[3:].replace('[','').replace(']','')
#     ct2Names = str(ShadowRaptor.CT2)[3:].replace('[','').replace(']','')
#     ftbuNames = str(ShadowRaptor.FTBUA)[3:].replace('[','').replace(']','')
#     obNames = str(ShadowRaptor.OB)[3:].replace('[','').replace(']','')
#     hexxitNames = str(ShadowRaptor.HEXXIT)[3:].replace('[','').replace(']','')

#     return dict({"player_count": totalCount,
#             "nomi_names": nomiNames,
#             "e6e_names": e6eNames,
#             "ct2_names": ct2Names,
#             "ftbu_names": ftbuNames,
#             "ob_names": obNames,
#             "hexxit_names": hexxitNames})

def updateData(home_servers_data):
    """
    Save changes to database and return template dictionary
    """
    ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.SERVERS, ['player_count'])
    ShadowRaptor.PLAYER_DATA.bulk_update(ShadowRaptor.SERVERS, ['player_names'])
    
    totalCount = str(ShadowRaptor.NETWORK)[0]
    nomiNames = str(ShadowRaptor.NOMI)[3:].replace('[','').replace(']','')
    e6eNames = str(ShadowRaptor.E6E)[3:].replace('[','').replace(']','')
    ct2Names = str(ShadowRaptor.CT2)[3:].replace('[','').replace(']','')
    ftbuNames = str(ShadowRaptor.FTBUA)[3:].replace('[','').replace(']','')
    obNames = str(ShadowRaptor.OB)[3:].replace('[','').replace(']','')
    hexxitNames = str(ShadowRaptor.HEXXIT)[3:].replace('[','').replace(']','')

    ShadowRaptor.LOGGER.error("playerCounts.py ran")

    return dict({"player_count": totalCount,
            "nomi_names": nomiNames,
            "e6e_names": e6eNames,
            "ct2_names": ct2Names,
            "ftbu_names": ftbuNames,
            "ob_names": obNames,
            "hexxit_names": hexxitNames})

def buffer():
    """
    Keep async operation away from database save
    """
    return asyncio.run(playerPoll())

async def playerPoll():
    """
    Asynchronously request Player data From MCAPI and make
    changes to the database
    """
    # home_servers_data = sync_to_async(update, thread_sensitive=False) 

    player_poller = PlayerCounts()
    player_data = player_poller.get_current_players()

    ShadowRaptor.NETWORK.player_count = player_data["totalCount"]
    ShadowRaptor.NOMI.player_count = player_data["nomi"]["count"]
    ShadowRaptor.NOMI.player_names = player_data["nomi"]["names"]
    ShadowRaptor.E6E.player_count = player_data["e6e"]["count"]
    ShadowRaptor.E6E.player_names = player_data["e6e"]["names"]
    ShadowRaptor.CT2.player_count = player_data["ct2"]["count"]
    ShadowRaptor.CT2.player_names = player_data["ct2"]["names"]
    ShadowRaptor.FTBUA.player_count = player_data["ftbu"]["count"]
    ShadowRaptor.FTBUA.player_names = player_data["ftbu"]["names"]
    ShadowRaptor.OB.player_count = player_data["ob"]["count"]
    
    
