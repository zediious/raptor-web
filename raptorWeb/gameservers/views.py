from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect

from os.path import join

from raptorWeb import settings
from gameservers.jobs import player_poller, update_context
from gameservers.models import Server

class Server_Buttons(TemplateView):
    """
    Returns Bootstrap buttons for each server
    Buttons used to open Server Modals
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverButtons.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Buttons_Loading(TemplateView):
    """
    Returns loading-image buttons for each server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverButtons_loading.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Modals(TemplateView):
    """
    Returns Bootstrap Modals for each server, containing
    all information regarding it
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverModals.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Total_Count(TemplateView):
    """
    Returns button showing total player count
    and Bootstrap Modal containing names of online players
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'playerCounts.html')
            update_context()
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Rules(TemplateView):
    """
    Returns a Bootstrap Accordion containing Server Rules
    for each Server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverRules.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Banned_Items(TemplateView):
    """
    Returns a Bootstrap Accordion containing Server Banned
    Items for each Server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverBannedItems.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Voting(TemplateView):
    """
    Returns a Bootstrap Accordion containing Server Voting
    Information for each Server
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverVoting.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

if settings.SCRAPE_SERVER_ANNOUNCEMENT:
    from raptorbot.models import ServerAnnouncement

    class Server_Announcements_Base(TemplateView):
        """
        Returns a Bootstrap Accordion containing Server Announcement
        Information for each Server
        """
        def get(self, request):
            if request.headers.get('HX-Request') == "true":
                template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverAnnouncements.html')
                return render(request, template_name, context=player_poller.currentPlayers_DB)
            else:
                return HttpResponseRedirect('../')

    class Server_Announcements(ListView):
        """
        ListView for all ServerAnnouncements
        """
        model = ServerAnnouncement

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

        def get_queryset(self):
            server = Server.objects.get(server_address=self.request.GET.get('server_address'))
            return ServerAnnouncement.objects.filter(server=server)

        def get(self, request, *args, **kwargs):
            if request.headers.get('HX-Request') == "true":
                return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('../../')