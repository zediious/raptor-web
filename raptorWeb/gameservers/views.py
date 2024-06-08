from os.path import join
from logging import getLogger
from typing import Any

from django.views.generic import DetailView, ListView, TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils.text import slugify
from django.contrib import messages
from django.conf import settings

from raptorWeb.panel.models import PanelLogEntry
from raptorWeb.gameservers.models import ServerManager, ServerStatistic, Server, Player, PlayerCountHistoric
from raptorWeb.gameservers.forms import StatisticFilterForm, StatisticFilterFormFireFox
from raptorWeb.raptormc.models import SiteInformation

import plotly.express as plot_express

LOGGER = getLogger('gameservers.views')
GAMESERVERS_TEMPLATE_DIR: str = getattr(settings, 'GAMESERVERS_TEMPLATE_DIR')
PANEL_TEMPLATE_DIR: str = getattr(settings, 'PANEL_TEMPLATE_DIR')


class Server_List_Base(ListView):
    """
    Base ListView for Server information
    """
    model: Server = Server

    def get_queryset(self) -> ServerManager:
        if 'loading' not in self.template_name:
            return Server.objects.get_servers()
        
        return Server.objects.get_servers(wait=False)

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('server'):
            try:
                context['opened_server_pk'] = int(self.request.GET.get('server'))
            except ValueError:
                context['opened_server_pk'] = self.request.GET.get('server')
        return context


class Server_Buttons(Server_List_Base):
    """
    Returns Bootstrap buttons for each server
    Buttons used to open Server Modals
    """
    paginate_by: int = 6
    
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        self.paginate_by = SiteInformation.objects.get_or_create(pk=1)[0].server_pagination_count
        return super().get(request, *args, **kwargs)


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
        
        
class Server_Onboarding(DetailView):
    """
    Onboarding view to be linked to players from the game server
    Contains all information regarding a server
    """
    model: Server = Server

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:     
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        else:
            return super().get(request, *args, **kwargs)

    def get_object(self):
        for server in Server.objects.filter(archived=False):
            if slugify(server.modpack_name) == self.kwargs['modpack_name']:
                return server
            
        return False
    
    
class Server_Description(TemplateView):
    """
    Return the server description of a requested server
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
            
        requested_server = request.GET.get('server').replace('onboarding/', '')
        all_servers = Server.objects.filter(archived=False)
        for server in all_servers:
            if slugify(server.modpack_name) == requested_server:
                return HttpResponse(server.server_description)
        
        LOGGER.error(
            f'Server description for {requested_server} was requested, but not found.'
        )
        return HttpResponse("No server found")
        
        
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
            markers=True,
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
        
        
class SetMaintenanceMode(View):
    """
    Toggle maintenance mode for a given server
    """
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('gameservers.maintenance_server'):
            messages.error(request, 'You do not have permission to change Maintenance status.')
            return HttpResponse(status=200)
        
        changing_server = Server.objects.get(pk=self.kwargs['pk'])
        if changing_server.in_maintenance:
            changing_server.in_maintenance = False
            
        else:
            changing_server.in_maintenance = True
        
        changing_server.save()
        messages.success(request, f'Maintenance status set to {changing_server.in_maintenance} for {changing_server}.')
        return render(request, template_name=join(PANEL_TEMPLATE_DIR, 'crud/panel_maintenance_button.html'), context={
            'maintenance_status': changing_server.in_maintenance,
            'server': changing_server
        })
        
        
class SetArchive(View):
    """
    Toggle archive for a given server
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('gameservers.archive_server'):
            messages.error(request, 'You do not have permission to change Archive status.')
            return HttpResponse(status=200)
        
        changing_server = Server.objects.get(pk=self.kwargs['pk'])
        if changing_server.archived:
            changing_server.archived = False
            
        else:
            changing_server.archived = True
        
        changing_server.save()
        messages.success(request, f'Archive status set to {changing_server.archived} for {changing_server}.')
        if 'archivedlist' in request.META['HTTP_REFERER']:
            return HttpResponseRedirect('/panel/api/html/panel/server/archivedlist')
        
        return HttpResponseRedirect('/panel/api/html/panel/server/list/')
    
    
class DeleteServer(View):
    """
    Permanently delete a given server
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('gameservers.delete_server'):
            messages.error(request, 'You do not have permission to delete servers.')
            return HttpResponse(status=200)
        
        changing_server = Server.objects.get(pk=self.kwargs['pk'])
        if changing_server.archived:
            messages.success(request, f'{changing_server} has been permanently deleted!')
            changing_server.delete()
            
            model_string = str(Server).split('.')[3].replace("'", "").replace('>', '')
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'{model_string} - {changing_server}'),
                action='Deleted'
            )
            
            return HttpResponseRedirect('/panel/api/html/panel/server/archivedlist')
            
        else:
            messages.error(request, f'There was an error attempting to delete {changing_server}!')
            return HttpResponse(status=200)


class Import_Servers(TemplateView):
    """
    Import servers
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('gameservers.importexport_server'):
            messages.error(request, 'You do not have permission to import and export servers.')
            return HttpResponse(status=200)
        
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
