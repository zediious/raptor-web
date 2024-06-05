from logging import getLogger

from django.conf import settings

from raptorWeb.raptormc.routes import Route
from raptorWeb.raptormc.models import InformativeText
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
    
    # If request is to root path, we do not need to check routes 
    if request.path == '/panel/':
        return True
                
    current_routes: list = []
    
    _get_main_routes()
    _get_server_routes()
    _get_informative_text_routes()
    
    for route in current_routes:
        first_slash = request.path.index('/')
        path = request.path[:first_slash]+request.path[first_slash+1:]
        if (str(route.name) == str(path)
        or str(f'{route.name}/') == str(path)):    
            return True    
        
    return False