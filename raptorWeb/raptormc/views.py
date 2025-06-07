from os.path import join
from logging import getLogger
from typing import Any

from django.views.generic import View, TemplateView, DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

from raptorWeb.raptormc.util.informative_text_factory import (
    get_or_create_informative_text
    )
from raptorWeb.raptormc.models import Page, DefaultPages, SiteInformation
from raptorWeb.raptormc.routes import check_route, CURRENT_URLPATTERNS

LOGGER = getLogger('raptormc.views')
TEMPLATE_DIR_RAPTORMC = getattr(settings, 'RAPTORMC_TEMPLATE_DIR')


class BaseView(TemplateView):
    """
    Base view for SPA
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'base.html')
    non_htmx: bool = True
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        route_result = check_route(request, CURRENT_URLPATTERNS, 'main')
        if route_result != False:
            return render(request, template_name=join(TEMPLATE_DIR_RAPTORMC, 'base.html'), context=route_result)
        
        return render(request, template_name=join(TEMPLATE_DIR_RAPTORMC, 'base.html'), context={"is_404": 'true'})
    

class DefaultPageTemplateView(TemplateView):
    """
    Take a DefaultPages attribute, return 404 if attribute is false on DefaultPages object
    """
    page_name: str = ''

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not DefaultPages.objects.get_enabled(self.page_name):
            return HttpResponseRedirect('/404')
            
        return super().get(request, *args, **kwargs)
    
class InformativeTemplateView(TemplateView):
    """
    Add list of passed informative texts to context, creating if non-existent.
    """
    informative_texts: list[str] = []

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context=context,
            informative_text_names=self.informative_texts)
    

class DefaultPageInformativeTemplateView(DefaultPageTemplateView):
    """
    Add list of passed informative texts to context, creating if non-existent.
    """
    informative_texts: list[str] = []

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return get_or_create_informative_text(
            context=context,
            informative_text_names=self.informative_texts)


class HomeServers(InformativeTemplateView):
    """
    Homepage with general information
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/home.html')
    informative_texts = ["Homepage Information"]


class Announcements(DefaultPageInformativeTemplateView):
    """
    Page containing the last 30 announcements from Discord
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/announcements.html')
    informative_texts = ["Announcements Information"]
    page_name = 'announcements'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update({"opened_server_pk": self.request.GET.get('server')})
        return context


class Rules(DefaultPageInformativeTemplateView):
    """
    Rules page containing general and server-specific rules
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/rules.html')
    informative_texts = ["Rules Information", "Network Rules"]
    page_name = 'rules'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update({"opened_server_pk": self.request.GET.get('server')})
        return context


class BannedItems(DefaultPageInformativeTemplateView):
    """
    Contains lists of items that are banned on each server
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/banneditems.html')
    informative_texts = ["Banneditems Information"]
    page_name = 'banned_items'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update({"opened_server_pk": self.request.GET.get('server')})
        return context


class Voting(DefaultPageInformativeTemplateView):
    """
    Contains lists links for each server's voting sites
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/voting.html')
    informative_texts = ["Voting Information"]
    page_name = 'voting'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update({"opened_server_pk": self.request.GET.get('server')})
        return context


class HowToJoin(DefaultPageInformativeTemplateView):
    """
    Contains guides for downloading modpacks and joining servers.
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/joining.html')
    informative_texts = [
                        "Howtojoin Information",
                        "Using the CurseForge Launcher",
                        "Using the FTB Launcher",
                        "Using the Technic Launcher"
                        ]
    page_name = 'joining'


class Onboarding(DefaultPageInformativeTemplateView):
    """
    Onboarding page containing all info about a specific server
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, 'defaultpages/onboarding.html')
    informative_texts = ["Rules Information", "Network Rules"]
    page_name = 'onboarding'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        return context.update({"opened_server_pk": self.request.GET.get('server')})


class StaffApps(DefaultPageInformativeTemplateView):
    """
    Provide links to each staff application
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'staffapps.html'))
    informative_texts = ["Applications Information"]
    page_name = 'staff_apps'
        
        
class Donations(DefaultPageInformativeTemplateView):
    """
    Donation packages list
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'
        
        
class DonationsCheckout(DefaultPageInformativeTemplateView):
    """
    Donation package checkout
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations_checkout.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'
    
        
class DonationsSuccess(DefaultPageInformativeTemplateView):
    """
    Donation success page
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations_success.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'
    
    
class DonationsFailure(DefaultPageInformativeTemplateView):
    """
    Donation failure page
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations_failure.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'
        
        
class DonationsFailureInvalidUsername(DefaultPageInformativeTemplateView):
    """
    Donation failure page when Minecraft username is invalid
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations_invalid_username.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'
        
        
class DonationsFailureInvalidPrice(DefaultPageInformativeTemplateView):
    """
    Donation failure page when chosen price is below minimum
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations_invalid_price.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'

    
class DonationsAlreadyDonated(DefaultPageInformativeTemplateView):
    """
    Donation already made page
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('defaultpages', 'donations_already_made.html'))
    informative_texts = ["Donations Information"]
    page_name = 'donations'


class SiteMembers(DefaultPageInformativeTemplateView):
    """
    Provide links to each Site Member's profile
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('users', 'sitemembers.html'))
    informative_texts = ["User Information"]
    page_name = 'members'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
        if site_info.require_login_for_user_list:
            if request.user.is_anonymous:
                return render(request, template_name=join(TEMPLATE_DIR_RAPTORMC, 'login_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: 
        context: dict[str, Any] = super().get_context_data(**kwargs)
        get_data = self.request.GET
        if get_data.get('username'):
            context['filtered_username'] = self.request.GET.get('username')
        if get_data.get('is_staff'): 
            context['filtered_is_staff'] = self.request.GET.get('is_staff')
        if get_data.get('page'):
            context['filtered_page'] = self.request.GET.get('page')
            
        return get_or_create_informative_text(
            context=context,
            informative_text_names=["User Information"])


class User_Page(TemplateView):
    """
    Info about a User
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('users', 'user.html'))
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
        if site_info.require_login_for_user_list:
            if request.user.is_anonymous:
                return render(request, template_name=join(TEMPLATE_DIR_RAPTORMC, 'login_access.html'))
        
        return super().get(request, *args, **kwargs)


class User_Pass_Reset(TemplateView):
    """
    Page to reset user password
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('users', 'user_pass_reset.html'))

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context.update({
            "active_user_for_reset": self.request.path.split('/')[6],
            "active_user_password_reset_token": self.request.path.split('/')[7]
        })
        return context


class PageView(DetailView):
    """
    Generic view for user created pages
    """
    model: Page = Page

    def get_object(self):
        return Page.objects.get_slugged_page(self.kwargs['page_name'])
        
        
class Update_Headerbox_State(View):
    """
    Update session variable regarding Headerbox
    expansion state.
    """
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict[str, Any]) -> HttpResponse:

        try:
            if request.session['headerbox_expanded'] == 'false':
                request.session['headerbox_expanded'] = 'true'
            else:
                request.session['headerbox_expanded'] = 'false'
            return HttpResponse(" ")
            
        except KeyError:
            request.session['headerbox_expanded'] = 'false'
            return HttpResponse(" ")


class View_404(TemplateView):
    """
    Base Admin Panel view
    """
    template_name: str = join(TEMPLATE_DIR_RAPTORMC, join('404.html'))
    
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict[str, Any]) -> HttpResponse:
        return render(request, template_name=join(TEMPLATE_DIR_RAPTORMC, 'base.html'), context={"is_404": 'true'})


def handler404(request, *args, **argv):
    return HttpResponseRedirect('/404')
