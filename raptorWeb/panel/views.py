from os.path import join
from logging import getLogger
from typing import Any

from django.db.models.query import QuerySet
from django.db.models import Model
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from raptorWeb.raptormc.routes import check_route
from raptorWeb.panel.routes import CURRENT_URLPATTERNS
from raptorWeb.panel.forms import (
    PanelSettingsInformation, PanelSettingsFiles,
    PanelDefaultPages, PanelServerUpdateForm,
    PanelServerCreateForm, PanelPlayerFilterForm,
    PanelPlayerPaginateForm, PanelInformativeTextUpdateForm,
    PanelPageForm, PanelToastForm, PanelNavWidgetUpdateForm,
    PanelNavWidgetCreateForm, PanelDonationPackageUpdateForm,
    PanelDonationPackageCreateForm, PanelCreatedStaffApplicationForm,
    PanelUserUpdateForm, PanelUserProfileInfoUpdateForm,
    PanelDiscordUserInfoUpdateForm, PanelRaptorUserGroupForm,
)
from raptorWeb.raptormc.models import (
    SiteInformation, DefaultPages, InformativeText, Page, PageManager,
    NotificationToast, NavbarLink, NavbarDropdown, NavWidget, NavWidgetBar,
)
from raptorWeb.raptorbot.models import DiscordGuild, GlobalAnnouncement, ServerAnnouncement, SentEmbedMessage
from raptorWeb.donations.models import CompletedDonation, DonationPackage, DonationServerCommand, DonationDiscordRole
from raptorWeb.staffapps.models import SubmittedStaffApplication, CreatedStaffApplication, StaffApplicationField
from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo, DeletionQueueForUser, RaptorUserGroup
from raptorWeb.gameservers.models import Server, ServerManager, Player
from raptorWeb.panel.models import PanelLogEntry

LOGGER = getLogger('panel.views')
TEMPLATE_DIR_PANEL = getattr(settings, 'PANEL_TEMPLATE_DIR')
TEMPLATE_DIR_PANEL_CRUD = join(TEMPLATE_DIR_PANEL, 'crud')
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
        route_result = check_route(request, CURRENT_URLPATTERNS, 'panel')
        if route_result != False:
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_base.html'))
        
        return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_base.html'), context={"is_404": 'true'})
    

class PanelApiBaseView(TemplateView):
    """
    Base view for API templates
    """
    template_name: str
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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
        if not request.user.has_perm('raptormc.discord_bot_panel'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    
class ServerActionsPanel(PanelApiBaseView):
    """
    Server actions and configuration
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_serveractions.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('gameservers.importexport_server'):
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
    Page with site settings. Forms are returned to update all settings in Site Information.
    SettingsPanelFilePost and SettingsPanelDefaultPagesPost also accept POSTs from this View.
    """
    template_name: str = join(TEMPLATE_DIR_PANEL, 'panel_settings.html')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm('raptormc.settings'):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
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
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.settings'):
            return HttpResponseRedirect('/')
        
        settings_form: PanelSettingsInformation = PanelSettingsInformation(request.POST)

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
            
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'Site Settings - {changed_string[:-1]}'),
                action='Changed'
            )
            
            messages.success(request,
                             ('Settings have been successfully updated for the following: '
                              f'{changed_string[:-1]}'))
            
            return HttpResponse(status=200)

        else:
            
            messages.error(
                request,
                [f'{message[0].title().replace("_", " ")}: {message[1][0]}' for message in settings_form.errors.items()]
            )
            return HttpResponse(status=200)
        

class SettingsPanelFilePost(PanelApiBaseView):
    """
    Endpoint to submit files in the control panel
    """      
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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
            
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'Site Settings - {changed_string[:-1]}'),
                action='Changed'
            )
            
            messages.success(request,
                             ('The following new files have been successfully uploaded: '
                              f'{changed_string[:-1]}'))
            
            return HttpResponse(status=200)

        else:
            messages.error(
                request,
                [f'{message[0].title().replace("_", " ")}: {message[1][0]}' for message in settings_files_form.errors.items()]
            )
            
            return HttpResponse(status=400)
        
        
class SettingsPanelDefaultPagesPost(PanelApiBaseView):
    """
    Endpoint to submit boolean data about whether default pages are enabled
    """      
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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
            
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'Site Settings - {changed_string[:-1]}'),
                action='Changed'
            )
            
            messages.success(request,
                             ('The following Default Pages have had their state changed: '
                              f'{changed_string[:-1]}'))
            
            return HttpResponse(status=200)

        else:
            return HttpResponse(status=400)
        
"""
CRUD VIEWS

All below views are CRUD views for models in the application, used in the Control Panel

Generic Update, List, Create, Delete and Detail Views exist which are used by all model views.
"""

# Abstract Views
        
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
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        
        
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        model_form = self.get_form()
        model_form.instance = self.get_object()
        if model_form.is_valid():
            model_form_data = model_form.cleaned_data
            changed_object = self.get_object()
            changed: list = []
            changed_string: str = ""
            has_m2m = False
            has_o2o = False
            has_m2o = False
            
            for field in changed_object._meta.get_fields():
                field_string = str(field).replace(f'{self.model_classpath}.', '')
                if 'ManyToOneRel' in str(field.__class__):
                    has_m2o = True
                    continue
                
                if 'OneToOneRel' in str(field.__class__):
                    has_o2o = True
                    continue
                
                if 'ManyToManyField' in str(field.__class__):
                    has_m2m = True
                    continue
                
                if 'ManyToManyRel' in str(field.__class__):
                    has_m2m = True
                    continue

                if field_string not in self.ignored_fields:
                    if field_string in self.image_fields:
                        if model_form_data[field_string] != None:
                            changed.append(field_string.title().replace('_', ' '))

                        continue
                    
                    if getattr(changed_object, field_string) != model_form_data[field_string]:
                        changed.append(field_string.title().replace('_', ' '))
                
            for change in changed:
                changed_string += f'{change}, '
            if changed == []:
                if not has_m2m:
                    if not has_m2o:
                        if not has_o2o:
                            messages.error(request, 'You must change some details before updating them.')
                            return HttpResponse(status=200)

            model_form.save()
            message = ((f'The following fields have been successfully updated '
                        f'for {self.get_object()}:\n\n'
                        f'{changed_string[:-1]}'))
            if has_m2m:
                message = f'{message} Any ManyToMany fields that have changed.'
                
            if has_m2o:
                if 'ManyToMany' in message:
                    message = message.replace('ManyToMany', 'ManyToMany and ManyToOne')
                else:
                    message = f'{message} Any ManytoOne fields that have changed.'
                    
            if has_o2o:
                if 'ManyToOne' in message:
                    message = message.replace('ManyToOne', 'ManyToOne and OneToOne')
                elif 'ManyToMany' in message:
                    message = message.replace('ManyToMany', 'ManyToMany and OneToOne')
                else:
                    message = f'{message} Any OneToOne fields that have changed.'
            
            model_string = str(self.model).split('.')[3].replace("'", "").replace('>', '')
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'{model_string} - {self.get_object()} - {changed_string[:-1]}'),
                action='Changed'
            )

            messages.success(request, message)
            return HttpResponse(status=200)

        else:
            messages.error(
                request,
                [f'{message[0].title().replace("_", " ")}: {message[1][0]}' for message in model_form.errors.items()]
            )
            return HttpResponse(status=400)
        
        
class PanelListView(ListView):
    """
    Abstract ListView used in Panel CRUD views
    """
    permission: str = ''
    model_name: str = ''
    
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
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
    
    
class PanelListViewSearchable(PanelListView):
    """
    Abstract ListView used in Panel CRUD views
    Allows filtering by fields in ascending or descending direction
    """
    default_ordering: str = ''

    def get_queryset(self) -> QuerySet[Any]:
        queryset = self.model.objects.all().order_by(self.default_ordering)
        get = self.request.GET
        
        if get.get('order_by') != None:
            order_by = get.get('order_by').lower()
            direction = get.get('direction')
            if direction == 'desc':
                order_by = f'-{order_by}'
                
            queryset = queryset.order_by(order_by)
            
        if get.get('paginate_by') != None:
            self.paginate_by = get.get('paginate_by')
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_form = PanelPlayerPaginateForm
        paginate_data = {}
        get = self.request.GET

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
            'paginate_form': paginate_form(paginate_data),
        })
        return context
    
    
class PanelCreateView(CreateView):
    """
    Abstract CreateView used in Panel CRUD views
    """
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'generic_create.html')
    permission: str = ''
    redirect_url: str = ''
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.has_perm(self.permission):
            return HttpResponseRedirect('/')
            
        model_form = self.get_form()
        if model_form.is_valid():
            model_form.save()
            model_string = str(self.model).split('.')[3].replace("'", "")
            
            model_string = str(self.model).split('.')[3].replace("'", "").replace('>', '')
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'{model_string} - {model_form.instance}'),
                action='Created'
            )
            
            messages.success(
                request, f'A new {model_string.replace(">", "").title()} has been added!'
            )
            return HttpResponseRedirect(self.redirect_url)
        
        messages.error(
            request,
            [f'{message[0].title().replace("_", " ")}: {message[1][0]}' for message in model_form.errors.items()]
        )
        return HttpResponse(status=400)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'crud_url': self.crud_url,
            'model': self.model
        })
        return context
    

class PanelDeleteView(View):
    """
    Permanently delete a given list of objects
    """
    model: Model
    permission: str
    redirect_url: str

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        model_string = str(self.model).split('.')[3].replace("'", "").replace('>', '')
        
        if not request.user.has_perm(self.permission):
            messages.error(request, f'You do not have permission to delete {model_string}s.')
            return HttpResponse(status=200)
        
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken')
        deleting_objects = self.model.objects.filter(pk__in=form_data.keys())

        changed_string: str = ''
        deleting_objects_count = deleting_objects.count()
        if deleting_objects_count > 1:
            for model in deleting_objects:
                changed_string += f'{model}, '
                
        else:
            changed_string += f'{deleting_objects[0]}'
            
        if changed_string == '':
            messages.error(request, 'There were no objects to delete!')
            return HttpResponse(status=400)

        deleting_objects.delete()
        PanelLogEntry.objects.create(
            changing_user=request.user,
            changed_model=str(f'{model_string} - {changed_string}'),
            action='Deleted'
        )
        
        if deleting_objects_count > 1:
            messages.success(request, f'{model_string}s: {changed_string[:-2]} have been permanently deleted!')
        else:
            messages.success(request, f'{model_string}: {changed_string[:-2]} has been permanently deleted!')
            
        return HttpResponseRedirect(self.redirect_url)

    
class PanelDetailView(DetailView):
    """
    Abstract DetailView used in Panel CRUD views
    """
    permission: str = ''
    
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:     
        
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
# Panel Log Entry
    
class PanelLogEntryList(PanelListViewSearchable):
    """
    Return a list of Panel Log Entries for viewing
    """
    model: PanelLogEntry = PanelLogEntry
    paginate_by = 50
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'logentry_list.html')
    permission: str = 'panel.view_panellogentry'
    model_name: str = "PanelLogEntry"
    default_ordering: str = '-date'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'total_model_count': PanelLogEntry.objects.count()
            })

        return context
    
# Server

class PanelServerList(PanelListView):
    """
    Return a list of servers for viewing and accessing CRUD actions
    """
    model: Server = Server
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'server_list.html')
    permission: str = 'gameservers.view_server'
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
    crud_url: str = 'server'
    permission: str = 'gameservers.add_server'
        

class PanelServerUpdate(PanelUpdateView):
    """
    Return a list of server fields for editing.
    """
    model: Server = Server
    form_class = PanelServerUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'server_update.html')
    permission: str = 'gameservers.change_server'
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
    

class PanelServerDelete(PanelDeleteView):
    """
    Permanently delete a given list of Servers
    """
    model = Server
    permission = 'gameservers.delete_server'
    redirect_url = '/panel/api/html/panel/server/archivedlist'
    
# Player
    
class PanelPlayerList(PanelListViewSearchable):
    """
    Return a list of players that have joined servers for viewing and CRUD actions
    Allow filtering by username alongside PanelListViewSearchable parameters
    """
    model: Player = Player
    paginate_by = 50
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'player_list.html')
    permission: str = 'gameservers.view_player'
    model_name: str = "Player"
    default_ordering: str = '-last_online'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('username') != None:
            queryset = queryset.filter(name__icontains=self.request.GET.get('username'))
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'player_filter_form': PanelPlayerFilterForm({'username': self.request.GET.get('username')}),
                'total_model_count': Player.objects.count()
            })
        
        if self.request.GET.get('username') != None:
            context.update({
                'form_data': self.request.GET
            })
            
        return context
    
# Informative Text
    
class PanelInformativeTextList(PanelListView):
    """
    Used by Panel to display list of Informative Text's for editing
    """
    model: InformativeText = InformativeText
    permission: str = 'raptormc.view_informativetext'
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'informativetext_list.html')
    model_name: str = 'Informative Text'
    paginate_by = 50
    
    
class PanelInformativeTextUpdate(PanelUpdateView):
    """
    Update changed information for a given Informative Text
    """
    model: InformativeText = InformativeText
    form_class = PanelInformativeTextUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'informativetext_update.html')
    permission: str = 'raptormc.change_informativetext'
    model_classpath: str = 'raptormc.InformativeText'
    ignored_fields = [
        'id',
        'name'
    ]
    
# Page
    
class PanelPageList(PanelListView):
    """
    Return a list of pages for viewing and accessing CRUD actions
    """
    model: Page = Page
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'page_list.html')
    permission: str = 'raptormc.view_page'
    model_name: str = 'Page'

    def get_queryset(self) -> PageManager:
        return Page.objects.all()
    
    
class PanelPageUpdate(PanelUpdateView):
    """
    Update changed information for a given Page
    """
    model: Page = Page
    form_class = PanelPageForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'page_update.html')
    permission: str = 'raptormc.change_page'
    model_classpath: str = 'raptormc.Page'
    image_fields = [
        'page_css',
        'page_js'
    ]
    ignored_fields = [
        'id',
        'created',
        'show_gameservers'
    ]
    
    
class PanelPageCreate(PanelCreateView):
    """
    Return a form to create/add a new Page.
    """
    model: Page = Page
    form_class = PanelPageForm
    redirect_url: str = '/panel/api/html/panel/content/page/list'
    crud_url: str = 'content/page'
    permission: str = 'raptormc.add_page'
    
    
class PanelPageDelete(PanelDeleteView):
    """
    Permanently delete a given list of Pages
    """
    model = Page
    permission = 'raptormc.delete_page'
    redirect_url = '/panel/api/html/panel/content/page/list'
    
# Notification Toast

class PanelToastList(PanelListView):
    """
    Return a list of Notification Toasts for viewing and accessing CRUD actions
    """
    model: NotificationToast = NotificationToast
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'toast_list.html')
    permission: str = 'raptormc.view_notificationtoast'
    model_name: str = 'Toast'

    def get_queryset(self) -> QuerySet[Any]:
        return NotificationToast.objects.all()
    
    
class PanelToastUpdate(PanelUpdateView):
    """
    Update changed information for a given Notification Toast
    """
    model: NotificationToast = NotificationToast
    form_class = PanelToastForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'toast_update.html')
    permission: str = 'raptormc.change_notificationtoast'
    model_classpath: str = 'raptormc.NotificationToast'
    ignored_fields = [
        'id',
        'created'
    ]
    
    
class PanelToastCreate(PanelCreateView):
    """
    Return a form to create/add a new Notification Toast.
    """
    model: NotificationToast = NotificationToast
    form_class = PanelToastForm
    redirect_url: str = '/panel/api/html/panel/content/toast/list'
    crud_url: str = 'content/toast'
    permission: str = 'raptormc.add_notificationtoast'
    
    
class PanelToastDelete(PanelDeleteView):
    """
    Permanently delete a given list of Notification Toasts
    """
    model = NotificationToast
    permission = 'raptormc.delete_notificationtoast'
    redirect_url = '/panel/api/html/panel/content/toast/list'
    
# Navbar Link
    
class PanelNavbarLinkList(PanelListView):
    """
    Return a list of Navbar Links for viewing and accessing CRUD actions
    """
    model: NavbarLink = NavbarLink
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navbarlink_list.html')
    permission: str = 'raptormc.view_navbarlink'
    model_name: str = 'NavbarLink'

    def get_queryset(self) -> QuerySet[Any]:
        return NavbarLink.objects.all()
    
    
class PanelNarbarLinkUpdate(PanelUpdateView):
    """
    Update changed information for a given Navbar Link
    """
    model: NavbarLink = NavbarLink
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navbarlink_update.html')
    permission: str = 'raptormc.change_navbarlink'
    model_classpath: str = 'raptormc.NavbarLink'
    ignored_fields = [
        'id'
    ]
    fields = [
        'name',
        'url',
        'linked_page',
        'parent_dropdown',
        'priority',
        'new_tab',
        'enabled'
    ]
    
    
class PanelNarbarLinkCreate(PanelCreateView):
    """
    Return a form to create/add a new Navbar Link
    """
    model: NavbarLink = NavbarLink
    redirect_url: str = '/panel/api/html/panel/content/navbarlink/list'
    crud_url: str = 'content/navbarlink'
    permission: str = 'raptormc.add_navbarlink'
    fields = [
        'name',
        'url',
        'linked_page',
        'parent_dropdown',
        'priority',
        'new_tab',
        'enabled'
    ]
    
    
class PanelNavbarLinkDelete(PanelDeleteView):
    """
    Permanently delete a given list of Navbar Links
    """
    model = NavbarLink
    permission = 'raptormc.delete_navbarlink'
    redirect_url = '/panel/api/html/panel/content/navbarlink/list'
    
# Navbar Dropdown
    
class PanelNavbarDropdownList(PanelListView):
    """
    Return a list of Navbar Dropdowns for viewing and accessing CRUD actions
    """
    model: NavbarDropdown = NavbarDropdown
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navbardropdown_list.html')
    permission: str = 'raptormc.view_navbardropdown'
    model_name: str = 'NavbarDropdown'

    def get_queryset(self) -> QuerySet[Any]:
        return NavbarDropdown.objects.all()
    
    
class PanelNavbarDropdownUpdate(PanelUpdateView):
    """
    Update changed information for a given Navbar Dropdowns
    """
    model: NavbarDropdown = NavbarDropdown
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navbardropdown_update.html')
    permission: str = 'raptormc.change_navbardropdown'
    model_classpath: str = 'raptormc.NavbarDropdown'
    ignored_fields = [
        'id'
    ]
    fields = [
        'name',
        'priority',
        'enabled'
    ]
    
    
class PanelNavbarDropdownCreate(PanelCreateView):
    """
    Return a form to create/add a new Navbar Dropdown
    """
    model: NavbarDropdown = NavbarDropdown
    redirect_url: str = '/panel/api/html/panel/content/navbardropdown/list'
    crud_url: str = 'content/navbardropdown'
    permission: str = 'raptormc.add_navbardropdown'
    fields = [
        'name',
        'priority',
        'enabled'
    ]
    
    
class PanelNavbarDropdownDelete(PanelDeleteView):
    """
    Permanently delete a given list of Navbar Dropdowns
    """
    model = NavbarDropdown
    permission = 'raptormc.delete_navbardropdown'
    redirect_url = '/panel/api/html/panel/content/navbardropdown/list'
    
# Nav Widget
    
class PanelNavWidgetList(PanelListView):
    """
    Return a list of Nav Widgets for viewing and accessing CRUD actions
    """
    model: NavWidget = NavWidget
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navwidget_list.html')
    permission: str = 'raptormc.view_navwidget'
    model_name: str = 'NavWidget'

    def get_queryset(self) -> QuerySet[Any]:
        return NavWidget.objects.all()
    
    
class PanelNavWidgetUpdate(PanelUpdateView):
    """
    Update changed information for a given Nav Widget
    """
    model: NavWidget = NavWidget
    form_class: PanelNavWidgetUpdateForm = PanelNavWidgetUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navwidget_update.html')
    permission: str = 'raptormc.change_navwidget'
    model_classpath: str = 'raptormc.NavWidget'
    image_fields = [
        'nav_image'
    ]
    ignored_fields = [
        'id'
    ]
    
    
class PanelNavWidgetCreate(PanelCreateView):
    """
    Return a form to create/add a new Nav Widget
    """
    model: NavWidget = NavWidget
    form_class: PanelNavWidgetCreateForm = PanelNavWidgetCreateForm
    redirect_url: str = '/panel/api/html/panel/content/navwidget/list'
    crud_url: str = 'content/navwidget'
    permission: str = 'raptormc.add_navwidget'
    
    
class PanelNavWidgetDelete(PanelDeleteView):
    """
    Permanently delete a given list of Nav Widgets
    """
    model = NavWidget
    permission = 'raptormc.delete_navwidget'
    redirect_url = '/panel/api/html/panel/content/navwidget/list'
    
# Nav Widget Bar
    
class PanelNavWidgetBarList(PanelListView):
    """
    Return a list of Navwidget Bars for viewing and accessing CRUD actions
    """
    model: NavWidgetBar = NavWidgetBar
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navwidgetbar_list.html')
    permission: str = 'raptormc.view_navwidgetbar'
    model_name: str = 'NavWidgetBar'

    def get_queryset(self) -> QuerySet[Any]:
        return NavWidgetBar.objects.all()
    
    
class PanelNavWidgetBarUpdate(PanelUpdateView):
    """
    Update changed information for a given Nav Widget Bar
    """
    model: NavWidgetBar = NavWidgetBar
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'navwidgetbar_update.html')
    permission: str = 'raptormc.change_navwidgetbar'
    model_classpath: str = 'raptormc.NavWidgetBar'
    ignored_fields = [
        'id'
    ]
    fields = [
        'name',
        'priority',
        'enabled'
    ]
    
    
class PanelNavWidgetBarCreate(PanelCreateView):
    """
    Return a form to create/add a new Nav Widget Bar
    """
    model: NavWidgetBar = NavWidgetBar
    redirect_url: str = '/panel/api/html/panel/content/navwidgetbar/list'
    crud_url: str = 'content/navwidgetbar'
    permission: str = 'raptormc.add_navwidgetbar'
    fields = [
        'name',
        'priority',
        'enabled'
    ]
    
    
class PanelNavWidgetBarDelete(PanelDeleteView):
    """
    Permanently delete a given list of Nav Widget Bars
    """
    model = NavWidgetBar
    permission = 'raptormc.delete_navwidgetbar'
    redirect_url = '/panel/api/html/panel/content/navwidgetbar/list'
    
# Global Announcement
    
class PanelGlobalAnnouncementList(PanelListViewSearchable):
    """
    Return a list of Global Announcements for viewing and accessing CRUD actions
    """
    model: GlobalAnnouncement = GlobalAnnouncement
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'globalannouncement_list.html')
    permission: str = 'raptorbot.view_globalannouncement'
    model_name: str = 'GlobalAnnouncement'
    default_ordering: str = '-date'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_model_count': GlobalAnnouncement.objects.count()
        })
        return context
    
    
class PanelGlobalAnnouncementView(PanelDetailView):
    """
    Return details about a given Global Announcement
    """
    model: GlobalAnnouncement = GlobalAnnouncement
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'globalannouncement_view.html')
    permission: str = 'raptorbot.view_globalannouncement'
    

class PanelGlobalAnnouncementDelete(PanelDeleteView):
    """
    Permanently delete a given list of Global Announcements
    """
    model = GlobalAnnouncement
    permission = 'raptorbot.delete_globalannouncement'
    redirect_url = '/panel/api/html/panel/bot/globalannouncement/list'
    
# Server Announcement
    
class PanelServerAnnouncementList(PanelListViewSearchable):
    """
    Return a list of Server Announcements for viewing and accessing CRUD actions
    """
    model: ServerAnnouncement = ServerAnnouncement
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'serverannouncement_list.html')
    permission: str = 'raptorbot.view_serverannouncement'
    model_name: str = 'ServerAnnouncement'
    default_ordering: str = '-date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_model_count': ServerAnnouncement.objects.count()
        })
        return context
    
    
class PanelServerAnnouncementView(PanelDetailView):
    """
    Return details about a given Server Announcement
    """
    model: ServerAnnouncement = ServerAnnouncement
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'serverannouncement_view.html')
    permission: str = 'raptorbot.view_serverannouncement'
    
    
class PanelServerAnnouncementDelete(PanelDeleteView):
    """
    Permanently delete a given list of Server Announcements
    """
    model = ServerAnnouncement
    permission = 'raptorbot.delete_serverannouncement'
    redirect_url = '/panel/api/html/panel/bot/serverannouncement/list'
    
# Sent Embed Message
    
class PanelSentEmbedMessageList(PanelListView):
    """
    Return a list of Sent Embed Messages for viewing and accessing CRUD actions
    """
    model: SentEmbedMessage = SentEmbedMessage
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'sentembedmessage_list.html')
    permission: str = 'raptorbot.view_sentembedmessage'
    model_name: str = 'SentEmbedMessage'

    def get_queryset(self) -> QuerySet[Any]:
        return SentEmbedMessage.objects.all()
    
    
class PanelSentEmbedMessageDelete(PanelDeleteView):
    """
    Permanently delete a given list of Sent Embed Messages
    """
    model = SentEmbedMessage
    permission = 'raptorbot.delete_sentembedmessage'
    redirect_url = '/panel/api/html/panel/bot/sentembedmessage/list'
    
# Donation Package
    
class PanelDonationPackageList(PanelListView):
    """
    Return a list of Donation Packages for viewing and accessing CRUD actions
    """
    model: DonationPackage = DonationPackage
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'donationpackage_list.html')
    permission: str = 'donations.view_donationpackage'
    model_name: str = 'DonationPackage'

    def get_queryset(self) -> QuerySet[Any]:
        return DonationPackage.objects.all()
    
    
class PanelDonationPackageUpdate(PanelUpdateView):
    """
    Update changed information for a given Donation Package
    """
    model: DonationPackage = DonationPackage
    form_class = PanelDonationPackageUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'donationpackage_update.html')
    permission: str = 'donations.change_donationpackage'
    model_classpath: str = 'donations.DonationPackage'
    image_fields = [
        'package_picture'
    ]
    ignored_fields = [
        'id'
    ]
    
    
class PanelDonationPackageCreate(PanelCreateView):
    """
    Return a form to create/add a new Donation Package.
    """
    model: DonationPackage = DonationPackage
    form_class = PanelDonationPackageCreateForm
    redirect_url: str = '/panel/api/html/panel/donations/donationpackage/list'
    crud_url: str = 'donations/donationpackage'
    permission: str = 'donations.add_donationpackage'
    
    
class PanelDonationPackageDelete(PanelDeleteView):
    """
    Permanently delete a given list of Donation Packages
    """
    model = DonationPackage
    permission = 'donations.delete_donationpackage'
    redirect_url = '/panel/api/html/panel/donations/donationpackage/list'
    
# Donation Server Command
    
class PanelDonationServerCommandList(PanelListView):
    """
    Return a list of Donation Server Commands for viewing and accessing CRUD actions
    """
    model: DonationServerCommand = DonationServerCommand
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'donationservercommand_list.html')
    permission: str = 'donations.view_donationservercommand'
    model_name: str = 'DonationServerCommand'

    def get_queryset(self) -> QuerySet[Any]:
        return DonationServerCommand.objects.all()
    
    
class PanelDonationServerCommandUpdate(PanelUpdateView):
    """
    Update changed information for a given Donation Server Command
    """
    model: DonationServerCommand = DonationServerCommand
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'donationservercommand_update.html')
    permission: str = 'donations.change_donationservercommand'
    model_classpath: str = 'donations.DonationServerCommand'
    ignored_fields = [
        'id'
    ]
    fields = [
        'command'
    ]
    
    
class PanelDonationServerCommandCreate(PanelCreateView):
    """
    Return a form to create/add a new Donation Server Command.
    """
    model: DonationServerCommand = DonationServerCommand
    redirect_url: str = '/panel/api/html/panel/donations/donationservercommand/list'
    crud_url: str = 'donations/donationservercommand'
    permission: str = 'donations.add_donationservercommand'
    fields = [
        'command'
    ]
    
    
class PanelDonationServerCommandDelete(PanelDeleteView):
    """
    Permanently delete a given list of Donation Server Commands
    """
    model = DonationServerCommand
    permission = 'donations.delete_donationservercommand'
    redirect_url = '/panel/api/html/panel/donations/donationservercommand/list'
    
# Donation Discord Role

class PanelDonationDiscordRoleList(PanelListView):
    """
    Return a list of Donation Discord Roles for viewing and accessing CRUD actions
    """
    model: DonationDiscordRole = DonationDiscordRole
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'donationdiscordrole_list.html')
    permission: str = 'donations.view_donationdiscordrole'
    model_name: str = 'DonationDiscordRole'

    def get_queryset(self) -> QuerySet[Any]:
        return DonationDiscordRole.objects.all()
    
    
class PanelDonationDiscordRoleUpdate(PanelUpdateView):
    """
    Update changed information for a given Donation Discord Role
    """
    model: DonationDiscordRole = DonationDiscordRole
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'donationdiscordrole_update.html')
    permission: str = 'donations.change_donationdiscordrole'
    model_classpath: str = 'donations.DonationDiscordRole'
    ignored_fields = [
        'id'
    ]
    fields = [
        'name',
        'role_id'
    ]
    
    
class PanelDonationDiscordRoleCreate(PanelCreateView):
    """
    Return a form to create/add a new Donation Discord Role.
    """
    model: DonationDiscordRole = DonationDiscordRole
    redirect_url: str = '/panel/api/html/panel/donations/donationdiscordrole/list'
    crud_url: str = 'donations/donationdiscordrole'
    permission: str = 'donations.add_donationdiscordrole'
    fields = [
        'name',
        'role_id'
    ]
    
    
class PanelDonationDiscordRoleDelete(PanelDeleteView):
    """
    Permanently delete a given list of Donation Discord Roles
    """
    model = DonationDiscordRole
    permission = 'donations.delete_donationdiscordrole'
    redirect_url = '/panel/api/html/panel/donations/donationdiscordrole/list'
    
# Completed Donation
    
class PanelCompletedDonationList(PanelListViewSearchable):
    """
    Return a list of Completed Donations for viewing and accessing CRUD actions
    """
    model: CompletedDonation = CompletedDonation
    paginate_by = 15
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'completeddonation_list.html')
    permission: str = 'donations.view_completeddonation'
    model_name: str = 'CompletedDonation'
    default_ordering: str = '-donation_datetime'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_model_count': CompletedDonation.objects.count()
        })
        return context

class PanelCompletedDonationView(PanelDetailView):
    """
    Return details about a given Completed Donation
    """
    model: CompletedDonation = CompletedDonation
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'completeddonation_view.html')
    permission: str = 'donations.view_completeddonation'
    
class PanelCompletedDonationDelete(PanelDeleteView):
    """
    Permanently delete a given list of Completed Donations
    """
    model = CompletedDonation
    permission = 'donations.delete_completeddonation'
    redirect_url = '/panel/api/html/panel/donations/completeddonation/list'
    
# Submitted Staff Application
    
class PanelSubmittedStaffApplicationList(PanelListViewSearchable):
    """
    Return a list of Submitted Staff Applications for viewing and accessing CRUD actions
    """
    model: SubmittedStaffApplication = SubmittedStaffApplication
    paginate_by = 15
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'submittedstaffapplication_list.html')
    permission: str = 'staffapps.view_submittedstaffapplication'
    model_name: str = 'SubmittedStaffApplication'
    default_ordering: str = '-submitted_date'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_model_count': SubmittedStaffApplication.objects.count()
        })
        return context
    
    
class PanelSubmittedStaffApplicationView(PanelDetailView):
    """
    Return details about a given Submitted Staff Application
    """
    model: SubmittedStaffApplication = SubmittedStaffApplication
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'submittedstaffapplication_view.html')
    permission: str = 'staffapps.view_submittedstaffapplication'


class PanelSubmittedStaffApplicationDelete(PanelDeleteView):
    """
    Permanently delete a given list of Submitted Staff Applications
    """
    model = SubmittedStaffApplication
    permission = 'staffapps.delete_submittedstaffapplication'
    redirect_url = '/panel/api/html/panel/staffapps/submittedstaffapplication/list'
    
# Created Staff Application
    
class PanelCreatedStaffApplicationList(PanelListView):
    """
    Return a list of Created Staff Applications for viewing and accessing CRUD actions
    """
    model: CreatedStaffApplication = CreatedStaffApplication
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'createdstaffapplication_list.html')
    permission: str = 'staffapps.view_createdstaffapplication'
    model_name: str = 'CreatedStaffApplication'

    def get_queryset(self) -> QuerySet[Any]:
        return CreatedStaffApplication.objects.all()
    
    
class PanelCreatedStaffApplicationUpdate(PanelUpdateView):
    """
    Update changed information for a given Created Staff Application
    """
    model: CreatedStaffApplication = CreatedStaffApplication
    form_class = PanelCreatedStaffApplicationForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'createdstaffapplication_update.html')
    permission: str = 'staffapps.change_createdstaffapplication'
    model_classpath: str = 'staffapps.CreatedStaffApplication'
    ignored_fields = [
        'id'
    ]
    
    
class PanelCreatedStaffApplicationCreate(PanelCreateView):
    """
    Return a form to create/add a new Created Staff Application
    """
    model: CreatedStaffApplication = CreatedStaffApplication
    form_class = PanelCreatedStaffApplicationForm
    redirect_url: str = '/panel/api/html/panel/staffapps/createdstaffapplication/list'
    crud_url: str = 'staffapps/createdstaffapplication'
    permission: str = 'staffapps.add_createdstaffapplication'


class PanelCreatedStaffApplicationDelete(PanelDeleteView):
    """
    Permanently delete a given list of Created Staff Applications
    """
    model = CreatedStaffApplication
    permission = 'staffapps.delete_createdstaffapplication'
    redirect_url = '/panel/api/html/panel/staffapps/createdstaffapplication/list'
    
# Staff Application Field
    
class PanelStaffApplicationFieldList(PanelListView):
    """
    Return a list of Staff Application Fields for viewing and accessing CRUD actions
    """
    model: StaffApplicationField = StaffApplicationField
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'staffapplicationfield_list.html')
    permission: str = 'staffapps.view_staffapplicationfield'
    model_name: str = 'StaffApplicationField'

    def get_queryset(self) -> QuerySet[Any]:
        return StaffApplicationField.objects.all()
    
    
class PanelStaffApplicationFieldUpdate(PanelUpdateView):
    """
    Update changed information for a given Staff Application Field
    """
    model: StaffApplicationField = StaffApplicationField
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'staffapplicationfield_update.html')
    permission: str = 'staffapps.change_staffapplicationfield'
    model_classpath: str = 'staffapps.StaffApplicationField'
    ignored_fields = [
        'id'
    ]
    fields = [
        'name',
        'help_text',
        'widget',
        'priority'
    ]
    
    
class PanelStaffApplicationFieldCreate(PanelCreateView):
    """
    Return a form to create/add a new Staff Application Field
    """
    model: StaffApplicationField = StaffApplicationField
    redirect_url: str = '/panel/api/html/panel/staffapps/staffapplicationfield/list'
    crud_url: str = 'staffapps/staffapplicationfield'
    permission: str = 'staffapps.add_staffapplicationfield'
    fields = [
        'name',
        'help_text',
        'widget',
        'priority'
    ]


class PanelStaffApplicationFieldDelete(PanelDeleteView):
    """
    Permanently delete a given list of Staff Application Fields
    """
    model = StaffApplicationField
    permission = 'staffapps.delete_staffapplicationfield'
    redirect_url = '/panel/api/html/panel/staffapps/staffapplicationfield/list'
    
# Raptor User
    
class PanelUserList(PanelListViewSearchable):
    """
    Return a list of Users registered on the website for viewing and CRUD actions
    Allow filtering by username alongside PanelListViewSearchable parameters
    """
    model: RaptorUser = RaptorUser
    paginate_by = 50
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'raptoruser_list.html')
    permission: str = 'authprofiles.view_raptoruser'
    model_name: str = "RaptorUser"
    default_ordering: str = '-date_joined'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('username') != None:
            queryset = queryset.filter(username__icontains=self.request.GET.get('username'))
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'user_filter_form': PanelPlayerFilterForm({'username': self.request.GET.get('username')}),
                'total_model_count': RaptorUser.objects.count()
            })
        
        if self.request.GET.get('username') != None:
            context.update({
                'form_data': self.request.GET
            })
            
        return context
    
    
class PanelUserUpdate(PanelUpdateView):
    """
    Return a list of User fields for editing.
    """
    model: RaptorUser = RaptorUser
    form_class = PanelUserUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'raptoruser_update.html')
    permission: str = 'authprofiles.change_raptoruser'
    model_classpath: str = 'authprofiles.RaptorUser'
    ignored_fields = [
        'id',
        'password',
        'totp_token',
        'totp_qr_path',
        'user_slug',
        'date_joined',
        'last_login',
        'is_discord_user',
        'date_queued_for_delete',
        'user_profile_info',
        'discord_user_info'
    ]
    
    
class PanelUserProfileInfoUpdate(PanelUpdateView):
    """
    Return a list of UserProfileInfo fields for editing.
    """
    model: UserProfileInfo = UserProfileInfo
    form_class = PanelUserProfileInfoUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'userprofileinfo_update.html')
    permission: str = 'authprofiles.change_userprofileinfo'
    model_classpath: str = 'authprofiles.UserProfileInfo'
    image_fields = ['profile_picture']
    ignored_fields = [
        'id',
        'picture_changed_manually'
    ]
    
    
class PanelDiscordUserInfoUpdate(PanelUpdateView):
    """
    Return a list of DiscordUserInfo fields for editing.
    """
    model: DiscordUserInfo = DiscordUserInfo
    form_class = PanelDiscordUserInfoUpdateForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'discorduserinfo_update.html')
    permission: str = 'authprofiles.change_discorduserinfo'
    model_classpath: str = 'authprofiles.DiscordUserInfo'
    ignored_fields = [
        'id',
        'tag',
        'pub_flags',
        'flags',
        'locale',
        'mfa_enabled'
    ]
    
    
class PanelUserDelete(PanelDeleteView):
    """
    Permanently delete a given list of Raptor Users
    """
    model = RaptorUser
    permission = 'authprofiles.delete_raptoruser'
    redirect_url = '/panel/api/html/panel/users/raptoruser/list'
    
# Raptor User Group

class PanelRaptorUserGroupList(PanelListView):
    """
    Return a list of RaptorUser Groups for viewing and accessing CRUD actions
    """
    model: RaptorUserGroup = RaptorUserGroup
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'raptorusergroup_list.html')
    permission: str = 'authprofiles.view_raptorusergroup'
    model_name: str = 'RaptorUserGroup'

    def get_queryset(self) -> QuerySet[Any]:
        return RaptorUserGroup.objects.all()
    
    
class PanelRaptorUserGroupUpdate(PanelUpdateView):
    """
    Update changed information for a given RaptorUser Group
    """
    model: RaptorUserGroup = RaptorUserGroup
    form_class = PanelRaptorUserGroupForm
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'raptorusergroup_update.html')
    permission: str = 'authprofiles.change_raptorusergroup'
    model_classpath: str = 'staffapps.RaptorUserGroup'
    ignored_fields = [
        'id',
        'auth.Group.id',
        'auth.Group.name',
        'auth.Group.permissions',
        'authprofiles.RaptorUserGroup.group_ptr'
    ]
    

class PanelRaptorUserGroupCreate(PanelCreateView):
    """
    Return a form to create/add a new RaptorUser Group
    """
    model: RaptorUserGroup = RaptorUserGroup
    form_class = PanelRaptorUserGroupForm
    redirect_url: str = '/panel/api/html/panel/users/raptorusergroup/list'
    crud_url: str = 'users/raptorusergroup'
    permission: str = 'authprofiles.add_raptorusergroup'
    
    
class PanelRaptorUserGroupDelete(PanelDeleteView):
    """
    Permanently delete a given list of Raptor User Groups
    """
    model = RaptorUserGroup
    permission = 'authprofiles.delete_raptorusergroup'
    redirect_url = '/panel/api/html/panel/users/raptorusergroup/list'
    
# Deletion Queue For User
    
class PanelDeletionQueueForUserList(PanelListView):
    """
    Return a list of RaptorUser's that have requested deletion for viewing and accessing CRUD actions
    """
    model: DeletionQueueForUser = DeletionQueueForUser
    paginate_by = 10
    template_name: str = join(TEMPLATE_DIR_PANEL_CRUD, 'deletionqueue_list.html')
    permission: str = 'authprofiles.view_deletionqueueforuser'
    model_name: str = 'DeletionQueueForUser'

    def get_queryset(self) -> QuerySet[Any]:
        return DeletionQueueForUser.objects.all()
    
    
class PanelDeletionQueueForUserDelete(PanelDeleteView):
    """
    Permanently delete a given list of Queue users
    """
    model = DeletionQueueForUser
    permission = 'authprofiles.delete_deletionqueueforuser'
    redirect_url = '/panel/api/html/panel/users/deletionqueue/list'
