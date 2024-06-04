from logging import getLogger

from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings

from raptorWeb.raptormc.routes import Route

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
                current_routes.append(
                    Route(
                        name=f'panel/{pattern.name}',
                        route_type="main"
                    )
                )
    
    # If request is to root path, we do not need to check routes 
    if request.path == '/panel/':
        return True
                
    current_routes: list = []
    
    _get_main_routes()
    
    for route in current_routes:
        first_slash = request.path.index('/')
        path = request.path[:first_slash]+request.path[first_slash+1:]
        if (str(route.name) == str(path)
        or str(f'{route.name}/') == str(path)):    
            return True    
        
    return False