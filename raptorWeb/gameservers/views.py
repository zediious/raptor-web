from os.path import join

from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.conf import settings

from raptorWeb.gameservers.models import ServerStatistic, Server, Player

GAMESERVERS_TEMPLATE_DIR: str = getattr(settings, 'GAMESERVERS_TEMPLATE_DIR')
SCRAPE_SERVER_ANNOUNCEMENT: bool = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')


class Server_Buttons(ListView):
    """
    Returns Bootstrap buttons for each server
    Buttons used to open Server Modals
    """
    paginate_by = 6
    model = Server

    def get_queryset(self):
        return Server.objects.filter().order_by('-pk')

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')


class Server_Buttons_Loading(ListView):
    """
    Returns Bootstrap buttons for each server
    Display loading spinner in each button
    """
    paginate_by = 6
    model = Server

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')


class Server_Modals(ListView):
    """
    Returns Bootstrap Modals for each server, containing
    all information regarding it.
    """
    model = Server

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')


class Server_Rules(ListView):
    """
    Returns a Bootstrap Accordion containing Server Rules
    for each Server
    """
    model = Server

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')


class Server_Banned_Items(ListView):
    """
    Returns a Bootstrap Accordion containing Server Banned
    Items for each Server
    """
    model = Server

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')


class Server_Voting(ListView):
    """
    Returns a Bootstrap Accordion containing Server Voting
    Information for each Server
    """
    model = Server

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')


if SCRAPE_SERVER_ANNOUNCEMENT:


    class Server_Announcements_Base(ListView):
        """
        Returns a Bootstrap Accordion to contain Server Announcement
        Information for each Server
        """
        model = Server

        def get(self, request, *args, **kwargs):
            if request.headers.get('HX-Request') == "true":
                return super().get(request, *args, **kwargs)

            else:
                return HttpResponseRedirect('../../')


class Player_List(ListView):
    """
    Returns button showing total player count
    and Bootstrap Modal containing names of online players

    This view will also call the update_servers() method of
    the Server Manager.
    """
    model = Player

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stat_object"] = ServerStatistic.objects.get_or_create(name='gameservers-stat')[0]
        context["server_list"] = Server.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            Server.objects.update_servers()
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('../../')
