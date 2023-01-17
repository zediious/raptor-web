from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from os.path import join

from raptorWeb import settings
from gameservers.jobs import player_poller, update_context


class Server_Buttons(TemplateView):
    """
    Returns HTML of server buttons
    Attempts to fetch new info before sending
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverButtons.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Buttons_Loading(TemplateView):
    """
    Returns HTML of server buttons with loading image
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverButtons_loading.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Server_Modals(TemplateView):
    """
    Returns HTML of server modals, as well as player counts modal
    Attempts to fetch new info before sending
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'serverModals.html')
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')

class Total_Count(TemplateView):
    """
    Returns a simple HttpResponse with the total count of players on all servers
    """
    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            template_name = join(settings.GAMESERVERS_TEMPLATE_DIR, 'playerCounts.html')
            update_context()
            return render(request, template_name, context=player_poller.currentPlayers_DB)
        else:
            return HttpResponseRedirect('../')
