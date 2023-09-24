from logging import getLogger

from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.conf import settings

from raptorWeb.raptorbot.models import GlobalAnnouncement, ServerAnnouncement
from raptorWeb.raptorbot import botware

try:
    from raptorWeb.raptormc.models import DefaultPages
except ModuleNotFoundError:
    pass

USE_GLOBAL_ANNOUNCEMENT: bool = getattr(settings, 'USE_GLOBAL_ANNOUNCEMENT')

if USE_GLOBAL_ANNOUNCEMENT:
    from raptorWeb.gameservers.models import Server

LOGGER = getLogger('raptorbot.views')

class Global_Announcements(ListView):
    """
    ListView for all Global Announcements
    """
    paginate_by: int = 5
    model: GlobalAnnouncement = GlobalAnnouncement
    queryset: GlobalAnnouncement.objects = GlobalAnnouncement.objects.order_by('-date')

    def get_queryset(self) -> GlobalAnnouncement.objects:
        try:
            return GlobalAnnouncement.objects.all().order_by(
                '-date')[:self.kwargs['amount']]
            
        except KeyError:
            return GlobalAnnouncement.objects.all().order_by('-date')

    def get(self, request: HttpRequest, amount: int=0, *args, **kwargs) -> HttpResponse:
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].announcements:
                return HttpResponseRedirect('/404')
            
        except ModuleNotFoundError:
            pass
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')

class Server_Announcements(ListView):
        """
        ListView for all Server Announcements
        """
        paginate_by: int = 5
        model: ServerAnnouncement = ServerAnnouncement

        def get_context_data(self, **kwargs) -> dict:
            context: dict = super().get_context_data(**kwargs)
            context["current_listed_server"] = self.kwargs['server_pk']
            return context

        def get_queryset(self) -> ServerAnnouncement.objects:
            server: Server = Server.objects.get(pk=self.kwargs['server_pk'])
            return ServerAnnouncement.objects.filter(server=server).order_by('-date')

        def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
            try:
                if not DefaultPages.objects.get_or_create(pk=1)[0].announcements:
                    return HttpResponseRedirect('/404')
                
            except ModuleNotFoundError:
                pass
            
            if request.headers.get('HX-Request') == "true":
                return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')


class Start_Bot(TemplateView):
    """
    Start the Discord Bot if it is stopped
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == True:
            return HttpResponse('<div class= "alert alert-danger">You cannot start the Discord Bot when it is currently running</div>')
        
        botware.start_bot_process()
        return HttpResponse('<div class= "alert alert-success">The Discord Bot has been started.</div>')


class Stop_Bot(TemplateView):
    """
    Stop the Discord Bot if it is currently running
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            return HttpResponse('<div class= "alert alert-danger">You cannot stop the Discord Bot when it is not running</div>')
        
        botware.stop_bot_process()
        return HttpResponse('<div class= "alert alert-success">The Discord Bot has been stopped.</div>')


class Update_Global_Announcement(TemplateView):
    """
    Update DiscordTasks Model attribute update_global_announcements to True
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            return HttpResponse('<div class= "alert alert-danger">You cannot send commands to the Discord Bot when it is not running</div>')
        
        botware.send_command_update_global_announcements()
        return HttpResponse('<div class= "alert alert-success">The command "refresh_global_announcements" has been sent to the Discord Bot.</div>')


class Update_Server_Announcement(TemplateView):
    """
    Update DiscordTasks Model attribute update_server_announcements to True
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            return HttpResponse('<div class= "alert alert-danger">You cannot send commands to the Discord Bot when it is not running</div>')
        
        botware.send_command_update_all_server_announcements()
        return HttpResponse('<div class= "alert alert-success">The command "refresh_server_announcements" has been sent to the Discord Bot.</div>')


class Update_Members(TemplateView):
    """
    Update DiscordTasks Model attribute update_members to True
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            return HttpResponse('<div class= "alert alert-danger">You cannot send commands to the Discord Bot when it is not running</div>')
        
        botware.send_command_update_members()
        return HttpResponse('<div class= "alert alert-success">Member counts for the Discord Guild have been updated.</div>')
