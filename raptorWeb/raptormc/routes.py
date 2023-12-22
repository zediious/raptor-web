from logging import getLogger

from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings

from raptorWeb.raptormc.models import Page, SiteInformation, InformativeText
from raptorWeb.authprofiles.models import RaptorUser
from raptorWeb.gameservers.models import Server
from raptorWeb.donations.models import DonationPackage

LOGGER = getLogger('raptormc.routes')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
CURRENT_URLPATTERNS = []

class Route:
    
    def __init__(self, name, route_type, informative_text=None, user=None, page=None, server=None, package=None) -> None:
        self.name: str = name
        self.route_type: str = route_type
        self.informative_text = informative_text
        self.user: RaptorUser = user
        self.page: Page = page
        self.server: Server = server
        self.package: DonationPackage = package
          
    def __str__(self) -> str:
        return self.name

def check_route(request):
    """
    Check all baked-in URLPatterns as well as
    variations for created objects. Return context
    with OpenGraph information about the route
    if the route exists, False if it does not.
    """
    def _get_user_routes():
        """
        Iterate all users and create a Route for
        each user. If a user has an active password
        reset token, create a route for that as well.
        """
        all_users = RaptorUser.objects.all()
        for user in all_users:
            current_routes.append(
                Route(
                    name=f'user/{user.user_slug}',
                    route_type="user",
                    user=user,
                )
            )
            
            if user.password_reset_token:
                current_routes.append(
                    Route(
                        name=f'user/reset/{user.user_slug}/{user.password_reset_token}',
                        route_type="user_reset",
                        user=user,
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
                    name=f'pages/{slugify(page.name)}',
                    route_type="page",
                    page=page,
                )
            )
            
    def _get_server_routes():
        """
        Iterate all servers and create a Route for
        each page's onboarding process.
        """
        all_servers = Server.objects.filter(archived=False)
        for server in all_servers:
            current_routes.append(
                Route(
                    name=f'onboarding/{slugify(server.modpack_name)}',
                    route_type="server",
                    server=server,
                )
            )
            
    def _get_package_routes():
        """
        Iterate all packages and create a Route for
        each packages's checkout page
        """
        all_packages = DonationPackage.objects.all()
        for package in all_packages:
            current_routes.append(
                Route(
                    name=f'donations/checkout/{slugify(package.name)}',
                    route_type="package",
                    package=package,
                )
            )
            
    def _get_main_routes():
        """
        Iterate current URLPatterns and create
        Routes for each. If the URLPattern name
        matches an Informative Text, attach that
        Informative Text to the route.
        """          
        informative_texts = InformativeText.objects.all()
        
        for pattern in CURRENT_URLPATTERNS[0]:
            gathered_text = informative_texts.filter(name=f'{str(pattern.name).title()} Information')
            if gathered_text is not None:
                current_routes.append(
                    Route(
                        name=pattern.name,
                        route_type="main_with_text",
                        informative_text=gathered_text.first()
                    )
                )
            else: 
                current_routes.append(
                    Route(
                        name=pattern.name,
                        route_type="main"
                    )
                )
                
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
    
    try:
        site_avatar_url = f"{WEB_PROTO}://{DOMAIN_NAME}{site_info.avatar_image.url}"
    except ValueError:
        site_avatar_url = f"{WEB_PROTO}://{DOMAIN_NAME}/static/image/no_user.svg"
    
    # If request is to root path, we do not need to check routes 
    if request.path == '/':
        return {
            "og_color": site_info.main_color,
            "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}",
            "og_image": f"{site_avatar_url}",
            "og_title": f"{site_info.brand_name} | Home",
            "og_desc": site_info.meta_description
        }
                
    current_routes: list = []
    
    _get_main_routes()
    _get_user_routes()
    _get_page_routes()
    _get_server_routes()
    _get_package_routes()
    
    for route in current_routes:
        first_slash = request.path.index('/')
        path = request.path[:first_slash]+request.path[first_slash+1:]
        if (str(route.name) == str(path)
        or str(f'{route.name}/') == str(path)):
            
            if route.user != None:
                try:
                    user_avatar =  f"{WEB_PROTO}://{DOMAIN_NAME}{route.user.user_profile_info.profile_picture.url}"
                except ValueError:
                    user_avatar = site_avatar_url
                    
                return {
                    "og_user": route.user,
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{BASE_USER_URL}/{route.user.user_slug}",
                    "og_image": f"{user_avatar}",
                    "og_title": f"{site_info.brand_name} | {route.user.username}",
                    "og_desc": f"User Profile for {route.user.username}"
                }
                
            if route.page != None:
                return {
                    "og_page": route.page,
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{route.page.get_absolute_url()}",
                    "og_image": f"{site_avatar_url}",
                    "og_title": f"{site_info.brand_name} | {route.page.name}",
                    "og_desc": route.page.meta_description
                }
                
            if route.server != None:
                return {
                    "og_server": route.server,
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/onboarding/{slugify(route.server.modpack_name)}",
                    "og_image": f"{site_avatar_url}",
                    "og_title": f"{site_info.brand_name} | {route.server.modpack_name} Onboarding",
                    "og_desc": strip_tags(route.server.modpack_description)
                }
                
            if route.package != None:
                return {
                    "og_package": route.package,
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/donations/checkout{slugify(route.package.name)}",
                    "og_image": f"{site_avatar_url}",
                    "og_title": f"{site_info.brand_name} | {route.package.name}",
                    "og_desc": strip_tags(route.package.package_description)
                }
                
            if route.informative_text != None:              
                return {
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{path}",
                    "og_image": f"{site_avatar_url}",
                    "og_title": f"{site_info.brand_name} | {path.title()}",
                    "og_desc": strip_tags(route.informative_text.content)
                }
                
            return {
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{path}",
                "og_image": f"{site_avatar_url}",
                "og_title": f"{site_info.brand_name} | {path.title()}",
                "og_desc": site_info.meta_description
            }
        
        
    return False