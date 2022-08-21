from multiprocessing import context
from django.shortcuts import render
from os.path import join, getmtime
from time import time
import logging

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.util import checkDatabase
from raptormc.models import PlayerCount, PlayerName, Server
from raptormc.forms import AdminApp, ModApp

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

player_poller = PlayerCounts()

class ShadowRaptor():
    """
    Object containing different categories of views that are used
    across the website/application.
    """
    LOGGER = logging.getLogger(__name__)

    class Info():
        """
        Views that act as static pages of information
        """
        def home_servers(request):
            """
            Homepage with general information
            """
            playerPoll()
            save_models()

            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = player_poller.currentPlayers_DB)
        
        def rules(request):
            """
            Rules page containing general and server-specific rules
            """
            playerPoll()
            save_models()

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context = player_poller.currentPlayers_DB)
            
        def banned_items(request):
            """
            Contains lists of items that are banned on each server
            """
            playerPoll()
            save_models()

            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context = player_poller.currentPlayers_DB)

        def apps(request):
            """
            Provide links to each staff application
            """
            playerPoll()
            save_models()

            return render(request, join(settings.APPLICATIONS_DIR, 'staffapps.html'), context=player_poller.currentPlayers_DB)
        
    class Application():
        """
        Views that contain forms and applications
        """
        def mod_app(request):
            """
            Moderator Application
            """
            playerPoll()
            save_models()
            
            mod_app = ModApp()

            player_poller.currentPlayers_DB["mod_form"] = mod_app

            if request.method == "POST":

                mod_app = ModApp(request.POST)

                if mod_app.is_valid():

                    ShadowRaptor.LOGGER.error("Mod Application IS VALID!")
                    ShadowRaptor.LOGGER.error(mod_app.cleaned_data)

            return render(request, join(settings.APPLICATIONS_DIR, 'modapp.html'), context=player_poller.currentPlayers_DB)
            
        def admin_app(request):
            """
            Admin Application
            """
            playerPoll()
            save_models()
            
            admin_app = AdminApp()

            player_poller.currentPlayers_DB["admin_form"] = admin_app

            if request.method == "POST":

                admin_app = ModApp(request.POST)

                if admin_app.is_valid():

                    ShadowRaptor.LOGGER.error("Admin Application IS VALID!")
                    ShadowRaptor.LOGGER.error(admin_app.cleaned_data)

            return render(request, join(settings.APPLICATIONS_DIR, 'adminapp.html'), context=player_poller.currentPlayers_DB)

def after_integrity():
    """
    Gets server objects from the database, only to be run
    after database integrity has been confirmed.
    """
    ShadowRaptor.NOMI_STATE = Server.objects.get(server_name="nomi")
    ShadowRaptor.E6E_STATE = Server.objects.get(server_name="e6e")
    ShadowRaptor.CT2_STATE = Server.objects.get(server_name="ct2")
    ShadowRaptor.FTBU_STATE = Server.objects.get(server_name="ftbu")
    ShadowRaptor.OB_STATE = Server.objects.get(server_name="ob")
    ShadowRaptor.HEXXIT_STATE = Server.objects.get(server_name="hexxit")

def playerPoll():
    """
    Request Player data From MCAPI and add PlayerName and PlayerCount
    objects to the database with a foreign key for each server. Will 
    only run if created .LOCK file hasn't been written to in 2 minutes. 
    Will confirm that Server objects exist, before getting them.
    """
    try:

        lock_time = time() - getmtime(join(settings.BASE_DIR, 'playerCounts.LOCK'))

        if  lock_time >= 120:
            
            player_data = player_poller.get_current_players()

            checkDatabase.confirm_database_integrity()

            after_integrity()

            PlayerCount.objects.all().delete()
            PlayerName.objects.all().delete()

            PlayerCount.objects.create(server=Server.objects.get(server_name="network"), player_count=player_data["totalCount"])

            totalCount = PlayerCount.objects.get(server=Server.objects.get(server_name="network")).player_count

            for key in player_data:

                if key == "totalCount":

                    continue

                for player in player_data[key]["names"]:

                    PlayerName.objects.create(server=Server.objects.get(server_name=key) , name=player)

                PlayerCount.objects.create(server=Server.objects.get(server_name=key), player_count=player_data[key]["count"])

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

            ShadowRaptor.LOGGER.error("[INFO] Request made, playerCounts.py ran")

        else:

            ShadowRaptor.LOGGER.error("[INFO] Request made, not enough time has passed to run playerCounts.py")

    except FileNotFoundError as e:

        ShadowRaptor.LOGGER.error(e)
        ShadowRaptor.LOGGER.error("[ERROR] playerCounts.LOCK file not present. Please create the file at the above path.")

def save_models():
    """
    Bulk update PlayerCount, PlayerName, and Server objects, specifically
    attributes from them that were modified while running playerPoll().
    """
    PlayerCount.objects.bulk_update(PlayerCount.objects.all(), ['player_count'])
    PlayerName.objects.bulk_update(PlayerName.objects.all(), ['name'])
    Server.objects.bulk_update(Server.objects.all(), ['server_state'])
