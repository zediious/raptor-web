from django.views.generic import ListView
from django.http import HttpResponseRedirect
from logging import getLogger

from raptorWeb import settings

from raptorbot.models import GlobalAnnouncement, ServerAnnouncement

if settings.USE_GLOBAL_ANNOUNCEMENT:
    from gameservers.models import Server

LOGGER = getLogger('raptorbot.views')

class Global_Announcements(ListView):
    """
    ListView for all ServerAnnouncements
    """
    model = GlobalAnnouncement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('../../')

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
