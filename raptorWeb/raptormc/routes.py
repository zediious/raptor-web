from logging import getLogger

from django.utils.text import slugify
from django.conf import settings

from raptorWeb.raptormc.models import Page, SiteInformation, InformativeText
from raptorWeb.authprofiles.models import RaptorUser

LOGGER = getLogger('raptormc.routes')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
CURRENT_URLPATTERNS = []

class Route:
    
    def __init__(self, name, route_type, user=None, page=None) -> None:
        self.name: str = name
        self.route_type: str = route_type
        self.user: RaptorUser = user
        self.page: Page = page
          
    def __str__(self) -> str:
        return self.name

def check_route(request):
    """
    Check all baked-in URLPatterns as well as
    variations for created objects. Return True
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
            
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
            
    current_routes: list = []
            
    if request.path == '/':
        return {
            "og_color": site_info.main_color,
            "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}",
            "og_image": f"{WEB_PROTO}://{DOMAIN_NAME}/{site_info.avatar_image.url}",
            "og_title": f"{site_info.brand_name} | Home",
            "og_desc": site_info.meta_description
        }
    
    for pattern in CURRENT_URLPATTERNS[0]:
        current_routes.append(
            Route(
                name=pattern.name,
                route_type="main"
            )
        )
        
    _get_user_routes()
    _get_page_routes()
    
    for route in current_routes:
        first_slash = request.path.index('/')
        path = request.path[:first_slash]+request.path[first_slash+1:]
        if (str(route.name) == str(path)
        or str(f'{route.name}/') == str(path)):
            if route.user != None:
                return {
                    "og_user": route.user,
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{BASE_USER_URL}/{route.user.user_slug}",
                    "og_image": f"{WEB_PROTO}://{DOMAIN_NAME}/{route.user.user_profile_info.profile_picture.url}",
                    "og_title": f"{site_info.brand_name} | {route.user.username}",
                    "og_desc": f"User Profile for {route.user.username}"
                }
                
            if route.page != None:
                return {
                    "og_page": route.page,
                    "og_color": site_info.main_color,
                    "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{route.page.get_absolute_url()}",
                    "og_image": f"{WEB_PROTO}://{DOMAIN_NAME}/{site_info.avatar_image.url}",
                    "og_title": f"{site_info.brand_name} | {route.page.name}",
                    "og_desc": route.page.meta_description
                }
                
            return {
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{path}",
                "og_image": f"{WEB_PROTO}://{DOMAIN_NAME}/{site_info.avatar_image.url}",
                "og_title": f"{site_info.brand_name} | {path.title()}",
                "og_desc": InformativeText.objects.get(
                    name=f"{path.title()} Information"
                )
            }
        
    return False