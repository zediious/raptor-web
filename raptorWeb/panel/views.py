from os.path import join
from logging import getLogger
from typing import Any

from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from raptorWeb.panel.routes import check_route
from raptorWeb.panel.forms import PanelSettingsInformation, PanelSettingsFiles, PanelDefaultPages
from raptorWeb.raptormc.models import SiteInformation, DefaultPages
from raptorWeb.raptorbot.models import DiscordGuild

LOGGER = getLogger('raptormc.views')
TEMPLATE_DIR_PANEL = getattr(settings, 'PANEL_TEMPLATE_DIR')
DISCORD_GUILD: int = getattr(settings, 'DISCORD_GUILD')


class BaseView(TemplateView):
    """
    Base view for Panel SPA
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_base.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.panel'):
            return HttpResponseRedirect('/')
        route_result = check_route(request)
        if route_result != False:
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_base.html'))
        
        return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_base.html'), context={"is_404": 'true'})
    

class PanelApiBaseView(TemplateView):
    """
    Base view for API templates
    """
    template_name: str
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.is_staff:
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
            
        return super().get(request, *args, **kwargs)


class HomePanel(PanelApiBaseView):
    """
    Homepage with general information
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_home.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.panel'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    

class DiscordBotPanel(PanelApiBaseView):
    """
    Discord bot actions and configuration
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_botactions.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.discord_bot'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    
class ServerActionsPanel(PanelApiBaseView):
    """
    Server actions and configuration
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_serveractions.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.server_actions'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)

   
class ReportingPanel(PanelApiBaseView):
    """
    Page with Reporting information
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_reporting.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.reporting'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    
class SettingsPanel(PanelApiBaseView):
    """
    Page with site settings
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_settings.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.settings'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        site_info = SiteInformation.objects.get_or_create(pk=1)[0]
        site_data = {
            'brand_name': site_info.brand_name,
            'contact_email': site_info.contact_email,
            'main_color': site_info.main_color,
            'use_main_color': site_info.use_main_color,
            'secondary_color': site_info.secondary_color,
            'use_secondary_color': site_info.use_secondary_color,
            'meta_description': site_info.meta_description,
            'meta_keywords': site_info.meta_keywords,
            'enable_footer': site_info.enable_footer,
            'enable_footer_credit': site_info.enable_footer_credit,
            'enable_footer_contact': site_info.enable_footer_contact,
            'require_login_for_user_list': site_info.require_login_for_user_list
        }
        
        default_pages = DefaultPages.objects.get_or_create(pk=1)[0]
        default_data = {
            'announcements': default_pages.announcements,
            'rules': default_pages.rules,
            'banned_items': default_pages.banned_items,
            'voting': default_pages.voting,
            'joining': default_pages.joining,
            'staff_apps': default_pages.staff_apps,
            'members': default_pages.members,
        }
            
        return render(request, template_name=self.template_name, context={
            'SettingsInformation': PanelSettingsInformation(site_data),
            'SettingsInformationFiles': PanelSettingsFiles(),
            'SettingsDefaultPages': PanelDefaultPages(default_data),
            'site_information': site_info,
            'discord_guild':  DiscordGuild.objects.get(guild_id=DISCORD_GUILD)
        })
        
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.settings'):
            return HttpResponseRedirect('/')
        
        settings_form: PanelSettingsInformation = PanelSettingsInformation(request.POST)
        dictionary: dict = {"SettingsInformation": settings_form}

        if settings_form.is_valid():
            changed: list = []
            changed_string: str = ""
            site_info = SiteInformation.objects.get_or_create(pk=1)[0]

            if site_info.brand_name != settings_form.cleaned_data['brand_name']:
                site_info.brand_name = settings_form.cleaned_data['brand_name']
                changed.append('Brand Name')

            if site_info.contact_email != settings_form.cleaned_data['contact_email']:
                site_info.contact_email = settings_form.cleaned_data['contact_email']
                changed.append('Contact Email')

            if site_info.main_color != settings_form.cleaned_data['main_color']:
                site_info.main_color = settings_form.cleaned_data['main_color']
                changed.append('Main Color')
                
            if site_info.use_main_color != settings_form.cleaned_data['use_main_color']:
                site_info.use_main_color = settings_form.cleaned_data['use_main_color']
                changed.append('Use Main Color')
                
            if site_info.secondary_color != settings_form.cleaned_data['secondary_color']:
                site_info.secondary_color = settings_form.cleaned_data['secondary_color']
                changed.append('Secondary Color')
                
            if site_info.use_secondary_color != settings_form.cleaned_data['use_secondary_color']:
                site_info.use_secondary_color = settings_form.cleaned_data['use_secondary_color']
                changed.append('Use Secondary Color')
                
            if site_info.meta_description != settings_form.cleaned_data['meta_description']:
                site_info.meta_description = settings_form.cleaned_data['meta_description']
                changed.append('Meta Description')
                
            if site_info.meta_keywords != settings_form.cleaned_data['meta_keywords']:
                site_info.meta_keywords = settings_form.cleaned_data['meta_keywords']
                changed.append('Meta Keywords')
                
            if site_info.enable_footer != settings_form.cleaned_data['enable_footer']:
                site_info.enable_footer = settings_form.cleaned_data['enable_footer']
                changed.append('Enable Footer')
                
            if site_info.enable_footer_credit != settings_form.cleaned_data['enable_footer_credit']:
                site_info.enable_footer_credit = settings_form.cleaned_data['enable_footer_credit']
                changed.append('Enable Footer Credit')
                
            if site_info.enable_footer_contact != settings_form.cleaned_data['enable_footer_contact']:
                site_info.enable_footer_contact = settings_form.cleaned_data['enable_footer_contact']
                changed.append('Enable Footer Contact')
                
            if site_info.require_login_for_user_list != settings_form.cleaned_data['require_login_for_user_list']:
                site_info.require_login_for_user_list = settings_form.cleaned_data['require_login_for_user_list']
                changed.append('Require Login for Member List')

            if changed == []:
                messages.error(request, 'You must change some values to update settings.')
                return render(request, self.template_name, context=dictionary)
            for change in changed:
                changed_string += f'{change}, '
            site_info.save()
            messages.success(request,
                             ('Settings have been successfully updated for the following: '
                              f'{changed_string[:-1]}'))
            
            return render(request, self.template_name, context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)
        

class SettingsPanelFilePost(PanelApiBaseView):
    """
    Endpoint to submit files in the control panel
    """      
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.settings'):
            return HttpResponseRedirect('/')
        
        settings_files_form: PanelSettingsFiles = PanelSettingsFiles(request.POST)
        dictionary: dict = {"SettingsInformationFiles": settings_files_form}
        site_info = SiteInformation.objects.get_or_create(pk=1)[0]

        if settings_files_form.is_valid():
            
            changed: list = []
            changed_string: str = ""
            if settings_files_form.cleaned_data['branding_image'] != None:
                site_info.branding_image = settings_files_form.cleaned_data['branding_image']
                changed.append('Branding Image')
                
            if settings_files_form.cleaned_data['background_image'] != None:
                site_info.background_image = settings_files_form.cleaned_data['background_image']
                changed.append('Background Image')
                
            if settings_files_form.cleaned_data['avatar_image'] != None:
                site_info.avatar_image = settings_files_form.cleaned_data['avatar_image']
                changed.append('Avatar Image')
                
            for change in changed:
                changed_string += f'{change}, '
            if changed == []:
                messages.error(request, 'You must change upload new files to update settings.')
                return render(request, self.template_name, context=dictionary)
            
            site_info.save()
            messages.success(request,
                             ('The following new files have been successfully uploaded: '
                              f'{changed_string[:-1]}'))
            
            return render(request, self.template_name, context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)
        
        
class SettingsPanelDefaultPagesPost(PanelApiBaseView):
    """
    Endpoint to submit boolean data about whether default pages are enabled
    """      
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.settings'):
            return HttpResponseRedirect('/')
        
        default_pages_form: PanelDefaultPages = PanelDefaultPages(request.POST)
        dictionary: dict = {"SettingsDefaultPages": default_pages_form}
        default_pages = DefaultPages.objects.get_or_create(pk=1)[0]

        if default_pages_form.is_valid():
            
            changed: list = []
            changed_string: str = ""
            if default_pages.announcements != default_pages_form.cleaned_data['announcements']:
                default_pages.announcements = default_pages_form.cleaned_data['announcements']
                changed.append('Announcements')
                
            if default_pages.rules != default_pages_form.cleaned_data['rules']:
                default_pages.rules = default_pages_form.cleaned_data['rules']
                changed.append('Rules')
                
            if default_pages.banned_items != default_pages_form.cleaned_data['banned_items']:
                default_pages.rules = default_pages_form.cleaned_data['banned_items']
                changed.append('Banned Items')
                
            if default_pages.voting != default_pages_form.cleaned_data['voting']:
                default_pages.voting = default_pages_form.cleaned_data['voting']
                changed.append('Voting')
                
            if default_pages.joining != default_pages_form.cleaned_data['joining']:
                default_pages.joining = default_pages_form.cleaned_data['joining']
                changed.append('Joining')
                
            if default_pages.staff_apps != default_pages_form.cleaned_data['staff_apps']:
                default_pages.staff_apps = default_pages_form.cleaned_data['staff_apps']
                changed.append('Staff Applications')
                
            if default_pages.members != default_pages_form.cleaned_data['members']:
                default_pages.members = default_pages_form.cleaned_data['members']
                changed.append('Site Members')
                
            for change in changed:
                changed_string += f'{change}, '
            if changed == []:
                messages.error(request, 'You must change the current settings before updating them.')
                return render(request, self.template_name, context=dictionary)
            
            default_pages.save()
            messages.success(request,
                             ('The following Default Pages have had their state changed: '
                              f'{changed_string[:-1]}'))
            
            return render(request, self.template_name, context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)
        
