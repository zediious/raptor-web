from logging import getLogger

from django.utils.text import slugify

from raptorWeb.raptormc.models import Page
from raptorWeb.authprofiles.models import RaptorUser

LOGGER = getLogger('raptormc.routes')

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
    current_routes: list = []
    
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
            
    if request.path == '/':
        return True
    
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
            return True
        
    return False