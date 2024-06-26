from logging import getLogger

from django.conf import settings

from raptorWeb.raptormc.routes import Route
from raptorWeb.raptormc.models import InformativeText, Page, NotificationToast, NavbarLink, NavbarDropdown, NavWidget, NavWidgetBar
from raptorWeb.raptorbot.models import GlobalAnnouncement, ServerAnnouncement
from raptorWeb.donations.models import DonationPackage, DonationServerCommand, DonationDiscordRole
from raptorWeb.staffapps.models import StaffApplicationField, SubmittedStaffApplication, CreatedStaffApplication
from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo, DeletionQueueForUser, RaptorUserGroup
from raptorWeb.gameservers.models import Server

LOGGER = getLogger('raptormc.routes')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
CURRENT_URLPATTERNS = []

def check_route(request):
    """
    Check all baked-in URLPatterns. Return True
    if the route exists, False if it does not.
    """       
    def _get_main_routes():
        """
        Iterate current URLPatterns and create
        Routes for each.
        """             
        for pattern in CURRENT_URLPATTERNS[0]:
                if '_IR' in pattern.name:
                    continue

                current_routes.append(
                    Route(
                        name=f'panel/{pattern.name}',
                        route_type="main"
                    )
                )

    def _get_server_routes():
        """
        Iterate all servers and create a Route for
        each server's update page.
        """
        all_servers = Server.objects.filter(archived=False)
        for server in all_servers:
            current_routes.append(
                Route(
                    name=f'panel/server/update/{server.pk}',
                    route_type="server",
                    server=server,
                )
            )
            
    def _get_informative_text_routes():
        """
        Iterate all Informative Texts and create a Route for
        each one's update page.
        """
        all_texts = InformativeText.objects.all()
        for text in all_texts:
            current_routes.append(
                Route(
                    name=f'panel/content/informativetext/update/{text.pk}',
                    route_type="informativetext",
                    informativetext=text
                )
            )
            
    def _get_page_routes():
        """
        Iterate all pages and create a Route for
        each page.
        """
        all_pages = Page.objects.all()
        for page in all_pages:
            current_routes.append(
                Route(
                    name=f'panel/content/page/update/{page.pk}',
                    route_type="page",
                    page=page,
                )
            )
            
    def _get_toast_routes():
        """
        Iterate all Notification Toasts and create a Route for
        each one.
        """
        all_toasts = NotificationToast.objects.all()
        for toast in all_toasts:
            current_routes.append(
                Route(
                    name=f'panel/content/toast/update/{toast.pk}',
                    route_type="notificationtoast",
                    toast=toast,
                )
            )
            
    def _get_navbarlink_routes():
        """
        Iterate all Navbar Links and create a Route for
        each one.
        """
        all_navbarlinks = NavbarLink.objects.all()
        for navbarlink in all_navbarlinks:
            current_routes.append(
                Route(
                    name=f'panel/content/navbarlink/update/{navbarlink.pk}',
                    route_type="navbarlink",
                    navbarlink=navbarlink,
                )
            )
            
    def _get_navbardropdown_routes():
        """
        Iterate all Navbar Dropdowns and create a Route for
        each one.
        """
        all_navbardropdowns = NavbarDropdown.objects.all()
        for dropdown in all_navbardropdowns:
            current_routes.append(
                Route(
                    name=f'panel/content/navbardropdown/update/{dropdown.pk}',
                    route_type="navbardropdown",
                    navbardropdown=dropdown,
                )
            )
            
    def _get_navwidget_routes():
        """
        Iterate all Nav Widgets and create a Route for
        each one.
        """
        all_navwidgets = NavWidget.objects.all()
        for widget in all_navwidgets:
            current_routes.append(
                Route(
                    name=f'panel/content/navwidget/update/{widget.pk}',
                    route_type="navwidget",
                    navwidget=widget,
                )
            )
            
    def _get_navwidgetbar_routes():
        """
        Iterate all Nav Widget Bars and create a Route for
        each one.
        """
        all_navwidgetbars = NavWidgetBar.objects.all()
        for bar in all_navwidgetbars:
            current_routes.append(
                Route(
                    name=f'panel/content/navwidgetbar/update/{bar.pk}',
                    route_type="navwidgetbar",
                    navwidgetbar=bar,
                )
            )
            
    def _get_globalannouncement_routes():
        """
        Iterate all Global Announcements and create a Route for
        each one.
        """
        all_globalannouncements = GlobalAnnouncement.objects.all()
        for announcement in all_globalannouncements:
            current_routes.append(
                Route(
                    name=f'panel/bot/globalannouncement/view/{announcement.pk}',
                    route_type="globalannouncement",
                    globalannouncement=announcement,
                )
            )
            
    def _get_serverannouncement_routes():
        """
        Iterate all Server Announcements and create a Route for
        each one.
        """
        all_serverannouncements = ServerAnnouncement.objects.all()
        for announcement in all_serverannouncements:
            current_routes.append(
                Route(
                    name=f'panel/bot/serverannouncement/view/{announcement.pk}',
                    route_type="serverannouncement",
                    serverannouncement=announcement,
                )
            )
            
    def _get_donationpackage_routes():
        """
        Iterate all Donation Packages and create a Route for
        each one.
        """
        all_donationpackages = DonationPackage.objects.all()
        for package in all_donationpackages:
            current_routes.append(
                Route(
                    name=f'panel/donations/donationpackage/update/{package.pk}',
                    route_type="donationpackage",
                    package=package,
                )
            )
            
    def _get_donationservercommand_routes():
        """
        Iterate all Donation Server Commands and create a Route for
        each one.
        """
        all_donationservercommands = DonationServerCommand.objects.all()
        for command in all_donationservercommands:
            current_routes.append(
                Route(
                    name=f'panel/donations/donationservercommand/update/{command.pk}',
                    route_type="donationservercommand",
                    donationservercommand=command,
                )
            )
            
    def _get_donationdiscordrole_routes():
        """
        Iterate all Donation Discord Roles and create a Route for
        each one.
        """
        all_donationdiscordroles = DonationDiscordRole.objects.all()
        for role in all_donationdiscordroles:
            current_routes.append(
                Route(
                    name=f'panel/donations/donationdiscordrole/update/{role.pk}',
                    route_type="donationdiscordrole",
                    donationdiscordrole=role,
                )
            )
            
    def _get_submittedstaffapplication_routes():
        """
        Iterate all Submitted Staff Applications and create a Route for
        each one.
        """
        all_submittedstaffapplication = SubmittedStaffApplication.objects.all()
        for application in all_submittedstaffapplication:
            current_routes.append(
                Route(
                    name=f'panel/staffapps/submittedstaffapplication/view/{application.pk}',
                    route_type="submittedstaffapplication",
                    submittedstaffapplication=application,
                )
            )
            
    def _get_createdstaffapplication_routes():
        """
        Iterate all Created Staff Applications and create a Route for
        each one.
        """
        all_createdstaffapplication = CreatedStaffApplication.objects.all()
        for application in all_createdstaffapplication:
            current_routes.append(
                Route(
                    name=f'panel/staffapps/createdstaffapplication/update/{application.pk}',
                    route_type="createdstaffapplication",
                    createdstaffapplication=application,
                )
            )
            
    def _get_staffapplicationfield_routes():
        """
        Iterate all Staff Application Fields and create a Route for
        each one.
        """
        all_staffapplicationfield = StaffApplicationField.objects.all()
        for form_field in all_staffapplicationfield:
            current_routes.append(
                Route(
                    name=f'panel/staffapps/staffapplicationfield/update/{form_field.pk}',
                    route_type="staffapplicationfield",
                    staffapplicationfield=form_field,
                )
            )
            
    def _get_raptoruseredit_routes():
        """
        Iterate all Raptor Users and create an update Route for
        each one.
        """
        all_raptorusers = RaptorUser.objects.all()
        for raptoruser in all_raptorusers:
            current_routes.append(
                Route(
                    name=f'panel/users/raptoruser/update/{raptoruser.pk}',
                    route_type="useredit",
                    useredit=raptoruser,
                )
            )
            
    def _get_userprofileinfo_routes():
        """
        Iterate all UserProfileInfo models and create an update Route for
        each one.
        """
        all_userprofileinfos = UserProfileInfo.objects.all()
        for profileinfo in all_userprofileinfos:
            current_routes.append(
                Route(
                    name=f'panel/users/userprofileinfo/update/{profileinfo.pk}',
                    route_type="userprofileinfo",
                    userprofileinfo=profileinfo,
                )
            )
            
    def _get_discorduserinfo_routes():
        """
        Iterate all DiscordUserInfo models and create an update Route for
        each one.
        """
        all_discorduserinfos = DiscordUserInfo.objects.all()
        for discordinfo in all_discorduserinfos:
            current_routes.append(
                Route(
                    name=f'panel/users/discorduserinfo/update/{discordinfo.pk}',
                    route_type="discorduserinfo",
                    discorduserinfo=discordinfo,
                )
            )
            
    def _get_raptorusergroup_routes():
        """
        Iterate all RaptorUser Groups and create an update Route for
        each one.
        """
        all_raptorusergroups = RaptorUserGroup.objects.all()
        for group in all_raptorusergroups:
            current_routes.append(
                Route(
                    name=f'panel/users/raptorusergroup/update/{group.pk}',
                    route_type="discorduserinfo",
                    raptorusergroup=group,
                )
            )
    
    # If request is to root path, we do not need to check routes 
    if request.path == '/panel/':
        return True
                
    current_routes: list = []
    
    _get_main_routes()
    _get_server_routes()
    _get_informative_text_routes()
    _get_page_routes()
    _get_toast_routes()
    _get_navbarlink_routes()
    _get_navbardropdown_routes()
    _get_navwidget_routes()
    _get_navwidgetbar_routes()
    _get_globalannouncement_routes()
    _get_serverannouncement_routes()
    _get_donationpackage_routes()
    _get_donationservercommand_routes()
    _get_donationdiscordrole_routes()
    _get_submittedstaffapplication_routes()
    _get_createdstaffapplication_routes()
    _get_staffapplicationfield_routes()
    _get_raptoruseredit_routes()
    _get_userprofileinfo_routes()
    _get_discorduserinfo_routes()
    _get_raptorusergroup_routes()
    
    for route in current_routes:
        first_slash = request.path.index('/')
        path = request.path[:first_slash]+request.path[first_slash+1:]
        if (str(route.name) == str(path)
        or str(f'{route.name}/') == str(path)):    
            return True    
        
    return False