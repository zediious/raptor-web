from logging import getLogger

from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.conf import settings

from raptorWeb.raptorbot.models import GlobalAnnouncement, ServerAnnouncement

USE_GLOBAL_ANNOUNCEMENT: bool = getattr(settings, 'USE_GLOBAL_ANNOUNCEMENT')

if USE_GLOBAL_ANNOUNCEMENT:
    from raptorWeb.gameservers.models import Server

LOGGER = getLogger('raptorbot.views')

class Global_Announcements(ListView):
    """
    ListView for all ServerAnnouncements
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
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')

class Server_Announcements(ListView):
        """
        ListView for all ServerAnnouncements
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
            if request.headers.get('HX-Request') == "true":
                return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')
