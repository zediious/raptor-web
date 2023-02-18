from os.path import join
from logging import getLogger

from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.conf import settings

from raptorWeb.raptormc.util.informative_text_factory import get_or_create_informative_text

TEMPLATE_DIR_RAPTORMC = getattr(settings, 'RAPTORMC_TEMPLATE_DIR')
USE_GLOBAL_ANNOUNCEMENT = getattr(settings, 'USE_GLOBAL_ANNOUNCEMENT')

LOGGER = getLogger('raptormc.views')


class HomeServers(TemplateView):
    """
    Homepage with general information
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, 'home.html')

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context, informative_text_names = ["Homepage Information"])


if USE_GLOBAL_ANNOUNCEMENT:
    class Announcements(TemplateView):
        """
        Page containing the last 30 announcements from Discord
        """
        template_name = join(TEMPLATE_DIR_RAPTORMC, 'announcements.html')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return get_or_create_informative_text(context = context, informative_text_names = ["Announcements Information"])


class Rules(TemplateView):
    """
    Rules page containing general and server-specific rules
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, 'rules.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context, informative_text_names = [
            "Rules Information",
            "Network Rules"])


class BannedItems(TemplateView):
    """
    Contains lists of items that are banned on each server
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, 'banneditems.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context, informative_text_names = ["Banned Items Information"])


class Voting(TemplateView):
    """
    Contains lists links for each server's voting sites
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, 'voting.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context, informative_text_names = ["Voting Information"])


class HowToJoin(TemplateView):
    """
    Contains guides for downloading modpacks and joining servers.
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, 'joining.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context, informative_text_names = [
            "Joining Information",
            "Using the CurseForge Launcher",
            "Using the FTB Launcher",
            "Using the Technic Launcher"])


class StaffApps(TemplateView):
    """
    Provide links to each staff application
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, join('applications', 'staffapps.html'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context, informative_text_names = ["Staff App Information"])


class SiteMembers(TemplateView):
    """
    Provide links to each Site Member's profile
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, join('users', 'sitemembers.html'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context)


class User_Page(TemplateView):
    """
    Info about a User
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, join('users', 'user.html'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return get_or_create_informative_text(context = context)


class User_Pass_Reset(TemplateView):
    """
    Page to reset user password
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, join('users', 'user_pass_reset.html'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "active_user_for_reset": self.request.path.split('/')[3],
            "active_user_password_reset_token": self.request.path.split('/')[4]
        })
        return get_or_create_informative_text(context = context)


class Admin_Panel(TemplateView):
    """
    Base Admin Panel view
    """
    template_name = join(TEMPLATE_DIR_RAPTORMC, join('panel', 'panel.html'))

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)
