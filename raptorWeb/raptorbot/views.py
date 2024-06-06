from os.path import join
from logging import getLogger

from django.views.generic import ListView, TemplateView, View
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings

from raptorWeb.gameservers.models import Server
from raptorWeb.raptorbot.models import GlobalAnnouncement, ServerAnnouncement, SentEmbedMessage
from raptorWeb.raptorbot import botware

try:
    from raptorWeb.raptormc.models import DefaultPages
except ModuleNotFoundError:
    pass

TEMPLATE_DIR_RAPTORBOT = getattr(settings, 'RAPTORBOT_TEMPLATE_DIR')

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
            
            
class Get_Bot_Status(TemplateView):
    """
    Return the status of the Discord bot
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.discord_bot'):
            return HttpResponseRedirect('/')
        
        if botware.get_bot_status() == True:
            return render(request, template_name=join(TEMPLATE_DIR_RAPTORBOT, 'bot_status_indicator.html'), context={
                'bot_status': 'on'
            })
            
        return render(request, template_name=join(TEMPLATE_DIR_RAPTORBOT, 'bot_status_indicator.html'), context={
                'bot_status': 'off'
            })


class Start_Bot(TemplateView):
    """
    Start the Discord Bot if it is stopped
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.discord_bot'):
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == True:
            messages.error(request, "You cannot start the Discord Bot when it is currently running.")
            return HttpResponse(status=204)
        
        if botware.is_safe_to_start() == False:
            messages.error(request, "You must wait one minute before restarting the bot.")
            return HttpResponse(status=204)
        
        botware.start_bot_process()
        messages.success(request, "The Discord Bot has been started.")
        return HttpResponse(status=204)


class Stop_Bot(TemplateView):
    """
    Stop the Discord Bot if it is currently running
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.discord_bot'):
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            messages.error(request, "You cannot stop the Discord Bot when it is not running.")
            return HttpResponse(status=204)
        
        botware.stop_bot_process()
        messages.success(request, "The Discord Bot has been stopped.")
        return HttpResponse(status=204)


class Update_Global_Announcement(TemplateView):
    """
    Update DiscordTasks Model attribute update_global_announcements to True
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.discord_bot'):
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            messages.error(request, "You cannot send commands to the Discord Bot when it is not running.")
            return HttpResponse(status=204)
        
        botware.send_command_update_global_announcements()
        messages.success(request, "The command 'refresh_global_announcements' has been sent to the Discord Bot.")
        return HttpResponse(status=204)


class Update_Server_Announcement(TemplateView):
    """
    Update DiscordTasks Model attribute update_server_announcements to True
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.discord_bot'):
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            messages.error(request, "You cannot send commands to the Discord Bot when it is not running.")
            return HttpResponse(status=204)
        
        botware.send_command_update_all_server_announcements()
        messages.success(request, "The command 'refresh_server_announcements' has been sent to the Discord Bot.")
        return HttpResponse(status=204)


class Update_Members(TemplateView):
    """
    Update DiscordTasks Model attribute update_members to True
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        return HttpResponseRedirect('/')

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.discord_bot'):
            return HttpResponseRedirect('/')

        if botware.get_bot_status() == False:
            messages.error(request, "You cannot send commands to the Discord Bot when it is not running.")
            return HttpResponse(status=204)
        
        messages.success(request, "Member counts for the Discord Guild have been updated.")
        return HttpResponse(status=204)
    
    
class GlobalAnnouncementDelete(View):
    """
    Permanently delete a given Global Announcement
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.globalannounce_delete'):
            messages.error(request, 'You do not have permission to delete Global Announcements.')
            return HttpResponse(status=200)
        
        changing_globalannouncement = GlobalAnnouncement.objects.get(pk=self.kwargs['pk'])
        changing_globalannouncement.delete()
            
        messages.success(request, f'{changing_globalannouncement} has been permanently deleted!')
        return HttpResponseRedirect('/panel/api/html/panel/bot/globalannouncement/list')
    
    
class ServerAnnouncementDelete(View):
    """
    Permanently delete a given Server Announcement
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.serverannounce_delete'):
            messages.error(request, 'You do not have permission to delete Server Announcements.')
            return HttpResponse(status=200)
        
        changing_serverannouncement = ServerAnnouncement.objects.get(pk=self.kwargs['pk'])
        changing_serverannouncement.delete()
            
        messages.success(request, f'{changing_serverannouncement} has been permanently deleted!')
        return HttpResponseRedirect('/panel/api/html/panel/bot/serverannouncement/list')
    
    
class SentEmbedMessageDelete(View):
    """
    Permanently delete a given Sent Embed Message
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.sentembedmessage_delete'):
            messages.error(request, 'You do not have permission to delete Sent Embed Messages.')
            return HttpResponse(status=200)
        
        changing_sentembedmessage = SentEmbedMessage.objects.get(pk=self.kwargs['pk'])
        changing_sentembedmessage.delete()
            
        messages.success(request, f'{changing_sentembedmessage} has been permanently deleted!')
        return HttpResponseRedirect('/panel/api/html/panel/bot/sentembedmessage/list')
