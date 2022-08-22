from django.shortcuts import render
from os.path import join

from raptorWeb import settings
from raptormc.util.playerCounts import PlayerCounts
from raptormc.forms import AdminApp, ModApp

TEMPLATE_DIR_RAPTORMC = join(settings.TEMPLATE_DIR, "raptormc")

player_poller = PlayerCounts()

class ShadowRaptor():
    """
    Object containing different categories of views that are used
    across the website/application.
    """
    class Info():
        """
        Views that act as static pages of information
        """
        def home_servers(request):
            """
            Homepage with general information
            """
            return render(request, join(TEMPLATE_DIR_RAPTORMC, "home.html"), context = player_poller.currentPlayers_DB)
        
        def rules(request):
            """
            Rules page containing general and server-specific rules
            """
            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'rules.html'), context = player_poller.currentPlayers_DB)
            
        def banned_items(request):
            """
            Contains lists of items that are banned on each server
            """
            return render(request, join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html'), context = player_poller.currentPlayers_DB)

        def apps(request):
            """
            Provide links to each staff application
            """
            return render(request, join(settings.APPLICATIONS_DIR, 'staffapps.html'), context=player_poller.currentPlayers_DB)
        
    class Application():
        """
        Views that contain forms and applications
        """
        def mod_app(request):
            """
            Moderator Application
            """
            mod_app = ModApp()

            dictionary = player_poller.currentPlayers_DB

            dictionary["modform"] = mod_app

            if request.method == "POST":

                mod_app = ModApp(request.POST)

                if mod_app.is_valid():

                    ShadowRaptor.LOGGER.error("[INFO] Mod Application submitted!")
                    ShadowRaptor.LOGGER.error("[INFO] Discord ID of applicant: {}".format(mod_app.cleaned_data["discord_name"]))
                    new_app = mod_app.save()
                    return render(request, join(settings.APPLICATIONS_DIR, 'appsuccess.html'), context=dictionary)

                else:

                    dictionary["modform"] = mod_app

            return render(request, join(settings.APPLICATIONS_DIR, 'modapp.html'), context=dictionary)
            
        def admin_app(request):
            """
            Admin Application
            """         
            admin_app = AdminApp()

            dictionary = player_poller.currentPlayers_DB

            dictionary["admin_form"] = admin_app

            if request.method == "POST":

                admin_app = AdminApp(request.POST)

                if admin_app.is_valid():

                    ShadowRaptor.LOGGER.error("[INFO] Admin Application submitted.!")
                    ShadowRaptor.LOGGER.error("[INFO] Discord ID of applicant: {}".format(admin_app.cleaned_data["discord_name"]))
                    new_app = admin_app.save()
                    return render(request, join(settings.APPLICATIONS_DIR, 'appsuccess.html'), context=dictionary)

                else:

                    dictionary["admin_form"] = admin_app

            return render(request, join(settings.APPLICATIONS_DIR, 'adminapp.html'), context=dictionary)
