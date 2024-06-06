from os.path import join
from logging import getLogger
from typing import Any

from django.apps import apps
from django.db.models.query import QuerySet
from django.db.models.fields.reverse_related import ManyToManyRel
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from raptorWeb.panel.routes import check_route
from raptorWeb.panel.forms import (PanelSettingsInformation, PanelSettingsFiles,
                                   PanelDefaultPages, PanelServerUpdateForm,
                                   PanelServerCreateForm, PanelPlayerFilterForm,
                                   PanelPlayerPaginateForm, PanelInformativeTextUpdateForm,
                                   PanelPageForm, PanelToastForm, PanelNavWidgetUpdateForm,
                                   PanelNavWidgetCreateForm, PanelDonationPackageUpdateForm,
                                   PanelDonationPackageCreateForm,)
from raptorWeb.raptormc.models import SiteInformation, DefaultPages, InformativeText, Page, PageManager, NotificationToast, NavbarLink, NavbarDropdown, NavWidget, NavWidgetBar
from raptorWeb.raptorbot.models import DiscordGuild, GlobalAnnouncement, ServerAnnouncement, SentEmbedMessage
from raptorWeb.donations.models import CompletedDonation, DonationPackage, DonationServerCommand, DonationDiscordRole
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
        model_form.instance = self.get_object()
        if model_form.is_valid():
            model_form_data = model_form.cleaned_data
            changed_object = self.get_object()
            changed: list = []
            changed_string: str = ""
            has_m2m = False
            has_m2o = False
            
            for field in changed_object._meta.get_fields():
                field_string = str(field).replace(f'{self.model_classpath}.', '')
                if 'ManyToOneRel' in str(field.__class__):
                    has_m2o = True
                    continue
                
                if 'ManyToManyField' or 'ManyToManyRel' in str(field.__class__):
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
                        messages.error(request, 'You must change some details before updating them.')
                        return HttpResponse(status=200)

            model_form.save()
            message = ((f'The following fields have been successfully updated '
                        f'for {self.get_object()}: '
                        f'{changed_string[:-1]}'))
            if has_m2m:
                message = f'{message} Any ManyToMany fields that have changed.'
                
            if has_m2o:
                message = message.replace('ManyToMany', 'ManyToMany and ManytoOne')
            
            model_string = str(self.model).split('.')[3].replace("'", "").replace('>', '')
            PanelLogEntry.objects.create(
                changing_user=request.user,
                changed_model=str(f'{model_string} - {self.get_object()}'),
                action='Changed'
            )

            messages.success(request, message)
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
    template_name_suffix = "_create_form"
    permission: str = ''
    redirect_url: str = ''
    
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
            request, [str(message[1][0]) for message in model_form.errors.items()]
        )
        return HttpResponse(status=200)

    
class PanelDetailView(DetailView):
    """
    Abstract DetailView used in Panel CRUD views
    """
    permission: str = ''
    
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:     
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm(self.permission):
            return render(request, template_name=join(TEMPLATE_DIR_PANEL, 'panel_no_access.html'))
        
        return super().get(request, *args, **kwargs)
    
    
class PanelLogEntryList(PanelListViewSearchable):
    """
    Return a list of Panel Log Entries for viewing
    """
    model: PanelLogEntry = PanelLogEntry
    paginate_by = 50
    permission: str = 'raptormc.logentry_list'
    model_name: str = "PanelLogEntry"
    default_ordering: str = '-date'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'total_panellogentry_count': PanelLogEntry.objects.count()
            })

        return context


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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'server_create.html'))
    redirect_url: str = '/panel/api/html/panel/server/list/'
    permission: str = 'raptormc.server_create'
        

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
    
    
class PanelPlayerList(PanelListViewSearchable):
    """
    Return a list of players that have joined servers for viewing and CRUD actions
    Allow filtering by username alongside PanelListViewSearchable parameters
    """
    model: Player = Player
    paginate_by = 50
    permission: str = 'raptormc.player_list'
    model_name: str = "Player"
    default_ordering: str = 'last_online'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        if self.request.GET.get('username') != None:
            queryset = queryset.filter(name__icontains=self.request.GET.get('username'))
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'player_filter_form': PanelPlayerFilterForm({'username': self.request.GET.get('username')})
            })
        
        if self.request.GET.get('username') != None:
            context.update({
                'form_data': self.request.GET
            })
            
        return context
    
    
class PanelInformativeTextList(PanelListView):
    """
    Used by Panel to display list of Informative Text's for editing
    """
    model: InformativeText = InformativeText
    permission: str = 'raptormc.informativetext_view'
    model_name: str = 'Informative Text'
    paginate_by = 50
    
    
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
    
class PanelPageList(PanelListView):
    """
    Return a list of pages for viewing and accessing CRUD actions
    """
    model: Page = Page
    paginate_by = 10
    permission: str = 'raptormc.page_list'
    model_name: str = 'Page'

    def get_queryset(self) -> PageManager:
        return Page.objects.all()
    
    
class PanelPageUpdate(PanelUpdateView):
    """
    Update changed information for a given Page
    """
    model: Page = Page
    form_class = PanelPageForm
    permission: str = 'raptormc.page_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'page_create.html'))
    redirect_url: str = '/panel/api/html/panel/content/page/list'
    permission: str = 'raptormc.page_create'
    

class PanelToastList(PanelListView):
    """
    Return a list of Notification Toasts for viewing and accessing CRUD actions
    """
    model: NotificationToast = NotificationToast
    paginate_by = 10
    permission: str = 'raptormc.toast_list'
    model_name: str = 'Toast'

    def get_queryset(self) -> QuerySet[Any]:
        return NotificationToast.objects.all()
    
    
class PanelToastUpdate(PanelUpdateView):
    """
    Update changed information for a given Notification Toast
    """
    model: NotificationToast = NotificationToast
    form_class = PanelToastForm
    permission: str = 'raptormc.toast_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'toast_create.html'))
    redirect_url: str = '/panel/api/html/panel/content/toast/list'
    permission: str = 'raptormc.toast_create'
    
    
class PanelNavbarLinkList(PanelListView):
    """
    Return a list of Navbar Links for viewing and accessing CRUD actions
    """
    model: NavbarLink = NavbarLink
    paginate_by = 10
    permission: str = 'raptormc.navbarlinks_list'
    model_name: str = 'NavbarLink'

    def get_queryset(self) -> QuerySet[Any]:
        return NavbarLink.objects.all()
    
    
class PanelNarbarLinkUpdate(PanelUpdateView):
    """
    Update changed information for a given Navbar Link
    """
    model: NavbarLink = NavbarLink
    permission: str = 'raptormc.navbarlinks_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'navbarlink_create.html'))
    redirect_url: str = '/panel/api/html/panel/content/navbarlink/list'
    permission: str = 'raptormc.navbarlink_create'
    fields = [
        'name',
        'url',
        'linked_page',
        'parent_dropdown',
        'priority',
        'new_tab',
        'enabled'
    ]
    
    
class PanelNavbarDropdownList(PanelListView):
    """
    Return a list of Navbar Dropdowns for viewing and accessing CRUD actions
    """
    model: NavbarDropdown = NavbarDropdown
    paginate_by = 10
    permission: str = 'raptormc.navbardropdown_list'
    model_name: str = 'NavbarDropdown'

    def get_queryset(self) -> QuerySet[Any]:
        return NavbarDropdown.objects.all()
    
    
class PanelNavbarDropdownUpdate(PanelUpdateView):
    """
    Update changed information for a given Navbar Dropdowns
    """
    model: NavbarDropdown = NavbarDropdown
    permission: str = 'raptormc.navbardropdown_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'navbardropdown_create.html'))
    redirect_url: str = '/panel/api/html/panel/content/navbardropdown/list'
    permission: str = 'raptormc.navbardropdown_create'
    fields = [
        'name',
        'priority',
        'enabled'
    ]
    
    
class PanelNavWidgetList(PanelListView):
    """
    Return a list of Nav Widgets for viewing and accessing CRUD actions
    """
    model: NavWidget = NavWidget
    paginate_by = 10
    permission: str = 'raptormc.navwidget_list'
    model_name: str = 'NavWidget'

    def get_queryset(self) -> QuerySet[Any]:
        return NavWidget.objects.all()
    
    
class PanelNavWidgetUpdate(PanelUpdateView):
    """
    Update changed information for a given Nav Widget
    """
    model: NavWidget = NavWidget
    form_class: PanelNavWidgetUpdateForm = PanelNavWidgetUpdateForm
    permission: str = 'raptormc.navwidget_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'navwidget_create.html'))
    redirect_url: str = '/panel/api/html/panel/content/navwidget/list'
    permission: str = 'raptormc.navwidget_create'
    
    
class PanelNavWidgetBarList(PanelListView):
    """
    Return a list of Navwidget Bars for viewing and accessing CRUD actions
    """
    model: NavWidgetBar = NavWidgetBar
    paginate_by = 10
    permission: str = 'raptormc.navwidgetbar_list'
    model_name: str = 'NavWidgetBar'

    def get_queryset(self) -> QuerySet[Any]:
        return NavWidgetBar.objects.all()
    
    
class PanelNavWidgetBarUpdate(PanelUpdateView):
    """
    Update changed information for a given Nav Widget Bar
    """
    model: NavWidgetBar = NavWidgetBar
    permission: str = 'raptormc.navwidgetbar_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'navwidgetbar_create.html'))
    redirect_url: str = '/panel/api/html/panel/content/navwidgetbar/list'
    permission: str = 'raptormc.navwidgetbar_create'
    fields = [
        'name',
        'priority',
        'enabled'
    ]
    
    
class PanelGlobalAnnouncementList(PanelListViewSearchable):
    """
    Return a list of Global Announcements for viewing and accessing CRUD actions
    """
    model: GlobalAnnouncement = GlobalAnnouncement
    paginate_by = 10
    permission: str = 'raptormc.globalannouncement_list'
    model_name: str = 'GlobalAnnouncement'
    default_ordering: str = 'date'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_globalannouncement_count': GlobalAnnouncement.objects.count()
        })
        return context
    
    
class PanelGlobalAnnouncementView(PanelDetailView):
    """
    Return details about a given Global Announcement
    """
    model: GlobalAnnouncement = GlobalAnnouncement
    permission: str = 'raptormc.globalannounce_view'
    
    
class PanelServerAnnouncementList(PanelListViewSearchable):
    """
    Return a list of Server Announcements for viewing and accessing CRUD actions
    """
    model: ServerAnnouncement = ServerAnnouncement
    paginate_by = 10
    permission: str = 'raptormc.serverannouncement_list'
    model_name: str = 'ServerAnnouncement'
    default_ordering: str = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_serverannouncement_count': ServerAnnouncement.objects.count()
        })
        return context
    
    
class PanelServerAnnouncementView(PanelDetailView):
    """
    Return details about a given Server Announcement
    """
    model: ServerAnnouncement = ServerAnnouncement
    permission: str = 'raptormc.serverannounce_view'
    
    
class PanelSentEmbedMessageList(PanelListView):
    """
    Return a list of Sent Embed Messages for viewing and accessing CRUD actions
    """
    model: SentEmbedMessage = SentEmbedMessage
    paginate_by = 10
    permission: str = 'raptormc.sentembedmessage_list'
    model_name: str = 'SentEmbedMessage'

    def get_queryset(self) -> QuerySet[Any]:
        return SentEmbedMessage.objects.all()
    
    
class PanelDonationPackageList(PanelListView):
    """
    Return a list of Donation Packages for viewing and accessing CRUD actions
    """
    model: DonationPackage = DonationPackage
    paginate_by = 10
    permission: str = 'raptormc.donationpackage_list'
    model_name: str = 'DonationPackage'

    def get_queryset(self) -> QuerySet[Any]:
        return DonationPackage.objects.all()
    
    
class PanelDonationPackageUpdate(PanelUpdateView):
    """
    Update changed information for a given Donation Package
    """
    model: DonationPackage = DonationPackage
    form_class = PanelDonationPackageUpdateForm
    permission: str = 'raptormc.donationpackage_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'donationpackage_create.html'))
    redirect_url: str = '/panel/api/html/panel/donations/donationpackage/list'
    permission: str = 'raptormc.donationpackage_create'
    
    
class PanelDonationServerCommandList(PanelListView):
    """
    Return a list of Donation Server Commands for viewing and accessing CRUD actions
    """
    model: DonationServerCommand = DonationServerCommand
    paginate_by = 10
    permission: str = 'raptormc.donationservercommand_list'
    model_name: str = 'DonationServerCommand'

    def get_queryset(self) -> QuerySet[Any]:
        return DonationServerCommand.objects.all()
    
    
class PanelDonationServerCommandUpdate(PanelUpdateView):
    """
    Update changed information for a given Donation Server Command
    """
    model: DonationServerCommand = DonationServerCommand
    permission: str = 'raptormc.donationservercommand_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'donationservercommand_create.html'))
    redirect_url: str = '/panel/api/html/panel/donations/donationservercommand/list'
    permission: str = 'raptormc.donationservercommand_create'
    fields = [
        'command'
    ]
    
    
class PanelDonationDiscordRoleList(PanelListView):
    """
    Return a list of Donation Discord Roles for viewing and accessing CRUD actions
    """
    model: DonationDiscordRole = DonationDiscordRole
    paginate_by = 10
    permission: str = 'raptormc.donationdiscordrole_list'
    model_name: str = 'DonationDiscordRole'

    def get_queryset(self) -> QuerySet[Any]:
        return DonationDiscordRole.objects.all()
    
    
class PanelDonationDiscordRoleUpdate(PanelUpdateView):
    """
    Update changed information for a given Donation Discord Role
    """
    model: DonationDiscordRole = DonationDiscordRole
    permission: str = 'raptormc.donationdiscordrole_update'
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
    template_name: str = join(TEMPLATE_DIR_PANEL, join('crud', 'donationdiscordrole_create.html'))
    redirect_url: str = '/panel/api/html/panel/donations/donationdiscordrole/list'
    permission: str = 'raptormc.donationdiscordrole_create'
    fields = [
        'name',
        'role_id'
    ]
    
    
class PanelCompletedDonationList(PanelListViewSearchable):
    """
    Return a list of Completed Donations for viewing and accessing CRUD actions
    """
    model: CompletedDonation = CompletedDonation
    paginate_by = 15
    permission: str = 'raptormc.completeddonation_list'
    model_name: str = 'CompletedDonation'
    default_ordering: str = '-donation_datetime'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_completeddonation_count': CompletedDonation.objects.count()
        })
        return context
    
