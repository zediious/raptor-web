from os.path import join

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.conf import settings

from raptorWeb.gameservers.models import Server

GAMESERVERS_TEMPLATE_DIR = getattr(settings, 'GAMESERVERS_TEMPLATE_DIR')
SCRAPE_SERVER_ANNOUNCEMENT = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')

class Server_Buttons(TemplateView):
    """
    Returns Bootstrap buttons for each server
    Buttons used to open Server Modals
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverButtons.html')
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

class Server_Buttons_Loading(TemplateView):
    """
    Returns loading-image buttons for each server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverButtons_loading.html')
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

class Server_Modals(TemplateView):
    """
    Returns Bootstrap Modals for each server, containing
    all information regarding it
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverModals.html')
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

class Total_Count(TemplateView):
    """
    Returns button showing total player count
    and Bootstrap Modal containing names of online players

    This view will also call the update_servers() method of
    the Server Manager.
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'playerCounts.html')
            Server.objects.update_servers()
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

class Server_Rules(TemplateView):
    """
    Returns a Bootstrap Accordion containing Server Rules
    for each Server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverRules.html')
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

class Server_Banned_Items(TemplateView):
    """
    Returns a Bootstrap Accordion containing Server Banned
    Items for each Server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverBannedItems.html')
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

class Server_Voting(TemplateView):
    """
    Returns a Bootstrap Accordion containing Server Voting
    Information for each Server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverVoting.html')
            return render(request, template_name, context={})
        else:
            return HttpResponseRedirect('../')

if SCRAPE_SERVER_ANNOUNCEMENT:

    class Server_Announcements_Base(TemplateView):
        """
        Returns a Bootstrap Accordion to contain Server Announcement
        Information for each Server
        """
        def get(self, request):
            if request.headers.get('HX-Request') == "true":
                template_name = join(GAMESERVERS_TEMPLATE_DIR, 'serverAnnouncements.html')
                return render(request, template_name, context={})
            else:
                return HttpResponseRedirect('../')
