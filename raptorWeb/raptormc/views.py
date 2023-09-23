from os.path import join
from logging import getLogger
from typing import Any

from django.views.generic import TemplateView, DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.conf import settings

from raptorWeb.raptormc.util.informative_text_factory import get_or_create_informative_text
from raptorWeb.raptormc.models import Page, DefaultPages

LOGGER = getLogger('raptormc.views')
TEMPLATE_DIR_RAPTORMC = getattr(settings, 'RAPTORMC_TEMPLATE_DIR')
USE_GLOBAL_ANNOUNCEMENT = getattr(settings, 'USE_GLOBAL_ANNOUNCEMENT')


class HomeServers(TemplateView):
    """
    Homepage with general information
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/home.html')

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context = context,
            informative_text_names = ["Homepage Information"])


if USE_GLOBAL_ANNOUNCEMENT:
    class Announcements(TemplateView):
        """
        Page containing the last 30 announcements from Discord
        """
        template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/announcements.html')
        
        def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].announcements:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)

        def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            return get_or_create_informative_text(
                context = context,
                informative_text_names = ["Announcements Information"])


class Rules(TemplateView):
    """
    Rules page containing general and server-specific rules
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/rules.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].rules:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context = context,
            informative_text_names = ["Rules Information", "Network Rules"])


class BannedItems(TemplateView):
    """
    Contains lists of items that are banned on each server
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/banneditems.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].banned_items:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context = context,
            informative_text_names = ["Banned Items Information"])


class Voting(TemplateView):
    """
    Contains lists links for each server's voting sites
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/voting.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].voting:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context = context,
            informative_text_names = ["Voting Information"])


class HowToJoin(TemplateView):
    """
    Contains guides for downloading modpacks and joining servers.
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/joining.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].joining:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context = context,
            informative_text_names = [
                "Joining Information",
                "Using the CurseForge Launcher",
                "Using the FTB Launcher",
                "Using the Technic Launcher"])


class StaffApps(TemplateView):
    """
    Provide links to each staff application
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('applications', 'staffapps.html'))
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].staff_apps:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context = context,
            informative_text_names = ["Staff App Information"])


class PageView(DetailView):
    """
    Generic view for user created pages
    """
    model: Page = Page

    def get_object(self):
        return Page.objects.get_slugged_page(self.kwargs['page_name'])


class SiteMembers(TemplateView):
    """
    Provide links to each Site Member's profile
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('users', 'sitemembers.html'))
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            if not DefaultPages.objects.get_or_create(pk=1)[0].members:
                return HttpResponseRedirect('/404')
            
            return super().get(request, *args, **kwargs)


class User_Page(TemplateView):
    """
    Info about a User
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('users', 'user.html'))


class User_Pass_Reset(TemplateView):
    """
    Page to reset user password
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('users', 'user_pass_reset.html'))

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        print(self.request.path.split('/')[3])
        print(self.request.path.split('/')[4])
        context.update({
            "active_user_for_reset": self.request.path.split('/')[3],
            "active_user_password_reset_token": self.request.path.split('/')[4]
        })
        return context


class Admin_Panel(TemplateView):
    """
    Base Admin Panel view
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('panel', 'panel.html'))

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict[str, Any]) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)


class View_404(TemplateView):
    """
    Base Admin Panel view
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('404.html'))


def handler404(request, *args, **argv):
    return HttpResponseRedirect('/404')
