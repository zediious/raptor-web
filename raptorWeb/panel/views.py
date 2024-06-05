from os.path import join
from logging import getLogger
from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from raptorWeb.panel.routes import check_route
from raptorWeb.panel.forms import PanelSettingsInformation, PanelSettingsFiles, PanelDefaultPages, PanelServerUpdateForm, PanelServerCreateForm, PanelPlayerFilterForm, PanelPlayerPaginateForm, PanelInformativeTextUpdateForm
from raptorWeb.raptormc.models import SiteInformation, DefaultPages, InformativeText
from raptorWeb.raptorbot.models import DiscordGuild
from raptorWeb.gameservers.models import Server, ServerManager, Player

LOGGER = getLogger('panel.views')
TEMPLATE_DIR_PANEL = getattr(settings, 'PANEL_TEMPLATE_DIR')
SETTINGS_FIELDS_TO_IGNORE = [
    'id',
    'branding_image',
    'branding_image_svg',
    'background_image',
    'avatar_image',
    'donation_goal_progress'
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
    
class DonationsPanel(PanelApiBaseView):
    """
    Server actions and configuration
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_donations.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.donations'):
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
                            changed.append(field_string.title().replace('_', ' ')) 
                    except KeyError:
                        continue
                    
            if (settings_form.cleaned_data['stripe_enabled'] == False
            and settings_form.cleaned_data['paypal_enabled'] == False):
                messages.error(request, 'You must have at least one Payment Gateway enabled.')
                return HttpResponse(status=200)
                        
            if changed == []:
                messages.error(request, 'You must change some values to update settings.')
                return HttpResponse(status=200)
            for change in changed:
                changed_string += f'{change}, '
            site_info.save()
            messages.success(request,
                             ('Settings have been successfully updated for the following: '
                              f'{changed_string[:-1]}'))
            
            return HttpResponse(status=200)

        else:
            
            messages.error(
                request, [str(message[1][0]) for message in settings_form.errors.items()]
            )
            return HttpResponse(status=200)
        

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
                
            if settings_files_form.cleaned_data['branding_image_svg'] != None:
                site_info.branding_image_svg = settings_files_form.cleaned_data['branding_image_svg']
                changed.append('Branding Image - SVG')
                
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
                return HttpResponse(status=200)
            
            site_info.save()
            messages.success(request,
                             ('The following new files have been successfully uploaded: '
                              f'{changed_string[:-1]}'))
            
            return HttpResponse(status=200)

        else:
            messages.error(request, [str(message[1][0]) for message in settings_files_form.errors.items()])
            return HttpResponse(status=400)
        
        
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
                        changed.append(field_string.title().replace('_', ' '))
                
            for change in changed:
                changed_string += f'{change}, '
            if changed == []:
                messages.error(request, 'You must change the current settings before updating them.')
                return HttpResponse(status=200)
            
            default_pages.save()
            messages.success(request,
                             ('The following Default Pages have had their state changed: '
                              f'{changed_string[:-1]}'))
            
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=400)
        
        
class PanelUpdateView(UpdateView):
    """
    Abstract UpdateView used in Panel CRUD views
    Overwrite post() to conform to SPA style. Messages
    are returned as HTTP headers to be picked up without
    refreshing the page
    """
    template_name_suffix = "_update_form"
    permission: str = ''
    model_classpath: str = ''
    image_fields: list = []
    ignored_fields: list = []

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        model_form = self.get_form()
        if model_form.is_valid():
            model_form_data = model_form.cleaned_data
            changed_object = self.get_object()
            changed: list = []
            changed_string: str = ""
            
            for field in self.model._meta.fields:
                field_string = str(field).replace(f'{self.model_classpath}.', '')
                if field_string not in self.ignored_fields:
                    if field_string in self.image_fields:
                        if model_form_data[field_string] != None:
                            setattr(
                                changed_object,
                                field_string,
                                model_form_data[field_string]
                            )
                            changed.append(field_string.title().replace('_', ' '))

                        continue

                    if getattr(changed_object, field_string) != model_form_data[field_string]:
                        setattr(
                            changed_object,
                            field_string,
                            model_form_data[field_string]
                        )
                        changed.append(field_string.title().replace('_', ' '))
                
            for change in changed:
                changed_string += f'{change}, '
            if changed == []:
                messages.error(request, 'You must change some details before updating them.')
                return HttpResponse(status=200)
            
            changed_object.save()

            messages.success(request,
                             ((f'The following fields have been successfully updated '
                               f'for {self.get_object()}: '
                               f'{changed_string[:-1]}')))
            return HttpResponse(status=200)

        else:  
            messages.error(
                request, [str(message[1][0]) for message in model_form.errors.items()]
            )
            return HttpResponse(status=200)
        
        
class PanelListView(ListView):
    """
    Abstract ListView used in Panel CRUD views
    """
    permission: str = ''
    model_name: str = ''
    
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.model,
            'model_name': self.model_name
        })
        return context
    
    
class PanelCreateView(CreateView):
    """
    Abstract CreateView used in Panel CRUD views
    """
    template_name_suffix = "_create_form"
    permission: str = ''
    redirect_url: str = ''
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm(self.permission):
            HttpResponseRedirect('/')
            
        model_form = self.get_form()
        if model_form.is_valid():
            model_form.save()
            model_string = str(self.model).split('.')[3].replace("'", "")
            messages.success(
                request, f'A new {model_string.replace(">", "").title()} has been added!'
            )
            return HttpResponseRedirect(self.redirect_url)


class PanelServerList(PanelListView):
    """
    Return a list of servers for viewing and accessing CRUD actions
    """
    model: Server = Server
    paginate_by = 10
    permission: str = 'raptormc.server_list'
    model_name: str = 'Server'

    def get_queryset(self) -> ServerManager:
        if 'archived' in self.request.path:
            return Server.objects.get_servers(wait=False,get_archived=True).reverse()
        
        return Server.objects.get_servers(wait=False).reverse()
        
        
class PanelServerCreate(PanelCreateView):
    """
    Return a form to create/add a new server.
    """
    model: Server = Server
    form_class = PanelServerCreateForm
    redirect_url: str = '/panel/api/html/panel/server/list/'
    permission: str = 'raptormc.server_update'
        

class PanelServerUpdate(PanelUpdateView):
    """
    Return a list of server fields for editing.
    """
    model: Server = Server
    form_class = PanelServerUpdateForm
    permission: str = 'raptormc.server_update'
    model_classpath: str = 'gameservers.Server'
    image_fields = ['modpack_picture']
    ignored_fields = [
        'id',
        'announcement_count',
        'in_maintenance',
        'server_state',
        'player_count',
        'archived'
    ]
    
    
class PanelPlayerList(PanelListView):
    """
    Return a list of players that have joined servers for viewing and CRUD actions
    """
    model: Player = Player
    paginate_by = 50
    permission: str = 'raptormc.player_list'
    model_name:str = "Player"
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Player.objects.all().order_by('-last_online')
        get = self.request.GET
        if get.get('username') != None:
            queryset = queryset.filter(name__icontains=get.get('username'))
        
        if get.get('order_by') != None:
            order_by = get.get('order_by')
            direction = get.get('direction')
            ordering = order_by.lower()
            if direction == 'desc':
                ordering = '-{}'.format(ordering)
                
            queryset = queryset.order_by(ordering)
            
        if get.get('paginate_by') != None:
            self.paginate_by = get.get('paginate_by')
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = PanelPlayerFilterForm
        paginate_form = PanelPlayerPaginateForm
        form_data = {}
        paginate_data = {}
        get = self.request.GET
        if get.get('username') != None:
            form_data.update({
                'username': get.get('username')
            })
            context.update({
                'form_data': get
            })
            
        if get.get('order_by') != None:
            context.update({
                'order_by': get.get('order_by'),
                'direction': get.get('direction')
            })
            
        if get.get('paginate_by') != None:
            context.update({
                'paginate_by': get.get('paginate_by')
            })
            paginate_data.update({
                'paginate_by': get.get('paginate_by')
            })
            
        else:
            context.update({
                'paginate_by': self.paginate_by
            })
            paginate_data.update({
                'paginate_by': self.paginate_by
            })
            
        context.update({
            'player_filter_form': filter_form(form_data),
            'player_paginate_form': paginate_form(paginate_data),
            'total_player_count': Player.objects.count()
        })
        return context
    
    
class PanelInformativeTextList(PanelListView):
    """
    Used by Panel to display list of Informative Text's for editing
    """
    model: InformativeText = InformativeText
    permission: str = 'raptormc.informativetext_view'
    model_name: str = 'Informative Text'
    paginate_by = 10
    
    
class PanelInformativeTextUpdate(PanelUpdateView):
    """
    Update changed information for a given Informative Text
    """
    model: InformativeText = InformativeText
    form_class = PanelInformativeTextUpdateForm
    permission: str = 'raptormc.informativetext_update'
    model_classpath: str = 'raptormc.InformativeText'
    ignored_fields = [
        'id',
        'name'
    ]
    
