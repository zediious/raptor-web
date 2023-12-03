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
SETTINGS_FIELDS_TO_IGNORE = [
    'id',
    'branding_image',
    'background_image',
    'avatar_image'
]


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
        site_data = {}
        for field in site_info._meta.fields:
            field_string = str(field).replace('raptormc.SiteInformation.', '')
            if field_string not in SETTINGS_FIELDS_TO_IGNORE:
                site_data.update({
                    field_string: getattr(site_info, field_string)
                })
        
        default_pages = DefaultPages.objects.get_or_create(pk=1)[0]
        default_data = {}
        for field in default_pages._meta.fields:
            field_string = str(field).replace('raptormc.DefaultPages.', '')
            default_data.update({
                field_string: getattr(default_pages, field_string)
            })
            
        return render(request, template_name=self.template_name, context={
            'SettingsInformation': PanelSettingsInformation(site_data),
            'SettingsInformationFiles': PanelSettingsFiles(),
            'SettingsDefaultPages': PanelDefaultPages(default_data),
            'site_information': site_info,
            'discord_guild':  DiscordGuild.objects.filter(guild_id=site_info.discord_guild).first()
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
            
            for field in site_info._meta.fields:
                field_string = str(field).replace('raptormc.SiteInformation.', '')
                if field_string not in SETTINGS_FIELDS_TO_IGNORE:
                    try:
                        if getattr(site_info, field_string) != settings_form.cleaned_data[field_string]:
                            setattr(
                                site_info,
                                field_string,
                                settings_form.cleaned_data[field_string]
                            )
                            changed.append(field_string.title()) 
                    except KeyError:
                        LOGGER.error(f'SitInformation field {field_string} was passed ' 
                                     'to form, but is not in the form.')
                        continue
                        
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
        
        settings_files_form: PanelSettingsFiles = PanelSettingsFiles(
            data=request.POST,
            files=request.FILES
        )
        dictionary: dict = {"SettingsInformationFiles": settings_files_form}
        site_info = SiteInformation.objects.get_or_create(pk=1)[0]

        if settings_files_form.is_valid():
            
            changed: list = []
            changed_string: str = ""
            if settings_files_form.cleaned_data['remove_branding_image'] == True:
                site_info.branding_image.delete(save=True)
                changed.append('Branding Image Deleted')
                
            if settings_files_form.cleaned_data['remove_background_image'] == True:
                site_info.background_image.delete(save=True)
                changed.append('Background Image Deleted')
                
            if settings_files_form.cleaned_data['remove_avatar_image'] == True:
                site_info.avatar_image.delete(save=True)
                changed.append('Avatar Image Deleted')
            
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
            
            for field in default_pages._meta.fields:
                field_string = str(field).replace('raptormc.DefaultPages.', '')
                if field_string not in SETTINGS_FIELDS_TO_IGNORE:
                    if getattr(default_pages, field_string) != default_pages_form.cleaned_data[field_string]:
                        setattr(
                            default_pages,
                            field_string,
                            default_pages_form.cleaned_data[field_string]
                        )
                        changed.append(field_string.title())
                
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
        
