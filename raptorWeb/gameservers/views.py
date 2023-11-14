from os.path import join
from logging import getLogger

from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from raptorWeb.gameservers.models import ServerManager, ServerStatistic, Server, Player, PlayerCountHistoric
from raptorWeb.gameservers.forms import StatisticFilterForm, StatisticFilterFormFireFox

import plotly.express as plot_express

LOGGER = getLogger('gameservers.views')
GAMESERVERS_TEMPLATE_DIR: str = getattr(settings, 'GAMESERVERS_TEMPLATE_DIR')
SCRAPE_SERVER_ANNOUNCEMENT: bool = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')
SERVER_PAGINATION_COUNT: int = getattr(settings, 'SERVER_PAGINATION_COUNT')


class Server_List_Base(ListView):
    """
    Base ListView for Server information
    """
    model: Server = Server

    def get_queryset(self) -> ServerManager:
        return Server.objects.filter(archived=False).order_by('-pk')

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')


class Server_Buttons(Server_List_Base):
    """
    Returns Bootstrap buttons for each server
    Buttons used to open Server Modals
    """
    paginate_by: int = SERVER_PAGINATION_COUNT


class Player_List(ListView):
    """
    Returns button showing total player count
    and Bootstrap Modal containing names of online players

    This view will also call the update_servers() method of
    the Server Manager.
    """
    model: Player = Player
    
    def get_queryset(self) -> Player.objects:
        return Player.objects.filter(online=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stat_object"] = ServerStatistic.objects.get_or_create(name='gameservers-stat')[0]
        context["server_list"] = Server.objects.filter(archived=False)
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            Server.objects.update_servers()
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
        
class Statistic_Filter_Form(TemplateView):
    """
    Return a form to submit server and date filter data
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.reporting'):
            return HttpResponseRedirect('/')
        
        if 'Firefox' not in str(request.META['HTTP_USER_AGENT']):
            return render(request, template_name=join(GAMESERVERS_TEMPLATE_DIR, 'player_statistics_form.html'), context={
                'stat_filter_form': StatisticFilterForm()})
            
        return render(request, template_name=join(GAMESERVERS_TEMPLATE_DIR, 'player_statistics_form.html'), context={
            'stat_filter_form': StatisticFilterFormFireFox()})
        
        
class Player_Count_Statistics(TemplateView):
    """
    Return a plotly chart containing PlayerCountHistoric data
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.reporting'):
            return HttpResponseRedirect('/')
        
        start = request.GET.get('start')
        end = request.GET.get('end')
        modpack_name = request.GET.get('server')
        
        try:
            found_server = Server.objects.get(modpack_name=modpack_name)
        except Server.DoesNotExist:
            messages.error(request, "Queried server not found")
            return HttpResponse(status=204)
        
        count_data = PlayerCountHistoric.objects.filter(server=found_server)
        
        if (start != '' and end != ''
        or start != '' or end != ''):
            if start == end and 'T' not in start:
                start += 'T00:00'
                end += 'T23:59'

        if start:
            count_data = count_data.filter(
                checked_time__gte=start
            )
            
        if end:
            count_data = count_data.filter(
                checked_time__lte=end
            )
        
        x_data = [count.checked_time for count in count_data]
        y_data = [count.player_count for count in count_data]
            
        if x_data == [] and y_data == []:
            messages.error(request, "No data found for selected range.")
            return HttpResponse(status=204)
        
        figure = plot_express.line(
            x=x_data,
            y=y_data,
            title="Player Counts over Time",
            template='plotly_dark',
            labels={'x': "Time of Query", 'y': 'Player Count'}
        )
        
        figure.update_layout(title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5
        })
        
        chart = figure.to_html()
        
        
        return render(request, template_name=join(GAMESERVERS_TEMPLATE_DIR, 'player_statistics_chart.html'), context={
            "chart": chart})


class Import_Servers(TemplateView):
    """
    Import servers
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.server_actions'):
            return HttpResponseRedirect('/')
        
        if Server.objects.import_server_data() == False:
            messages.error(request, ("You attempted to import servers, but you did not place server_data_full.json "
                                     "in the root directory of the application."))
            return HttpResponse(status=204)

        messages.success(request, "Servers from server_data_full.json have successfully been imported.")
        return HttpResponse(status=204)
        

class Export_Servers(TemplateView):
    """
    Export servers
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.server_actions'):
            return HttpResponseRedirect('/')
        
        Server.objects.export_server_data()
        messages.success(request, "All Servers have successfully been exported to server_data_full.json.")
        return HttpResponse(status=204)
