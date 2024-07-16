from logging import getLogger

from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings

from raptorWeb.raptormc.models import SiteInformation, InformativeText

LOGGER = getLogger('raptormc.routes')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
CURRENT_URLPATTERNS = []
ALL_ROUTED_MODELS = []


class Route:
    
    def __init__(self, name, route_type, model=None) -> None:
        
        self.name: str = name
        self.route_type: str = route_type
        self.model = model
          
    def __str__(self) -> str:
        return self.name
    

def check_route(request, patterns, app):
    """
    Check all baked-in URLPatterns as well as
    variations for created objects. Return context
    with information about the route or True if the
    route exists, False if it does not.
    """      
    def _get_models_routes(app=app):
        
        def _get_model_routes(routable_model, app):
            """
            Iterate all of a given routable model and create a Route for
            each object based on it's routing information
            """
            all_models = routable_model.objects.all()
            for model in all_models:
                if model.routes(app) == None:
                    continue
                
                if len(model.routes(app)) > 1:
                    for route in model.routes(app):
                        if len(route) > 1:
                            if not route[1]:
                                continue
                            
                        current_routes.append(
                            Route(
                                name=route[0],
                                route_type=model.route_name(),
                                model=model,
                            )
                        )
                        
                        if _verify_route(current_routes[-1]) != False:
                            found_route.append(current_routes[-1])
                            return current_routes[-1]
                                
                else:
                    if len(model.routes(app)[0]) > 1:
                        if not model.routes(app)[0][1]:
                            continue
                        
                    current_routes.append(
                        Route(
                            name=model.routes(app)[0][0],
                            route_type=model.route_name(),
                            model=model,
                        )
                    )

                    if _verify_route(current_routes[-1]) != False:
                        found_route.append(current_routes[-1])
                        return current_routes[-1]
                
        for model in ALL_ROUTED_MODELS:
            route = _get_model_routes(model, app)
            if route != None:
                return route
            
    def _get_main_routes():
        """
        Iterate current URLPatterns and create
        Routes for each. If the URLPattern name
        matches an Informative Text, attach that
        Informative Text to the route.
        """          
        informative_texts = InformativeText.objects.all()
        
        current_patterns = patterns[0]
        for pattern in current_patterns:
            if '_IR' in pattern.name:
                    continue
            
            gathered_text = informative_texts.filter(name=f'{str(pattern.name).title()} Information')
            if gathered_text is not None:
                current_routes.append(
                    Route(
                        name=pattern.name,
                        route_type="main_with_text",
                        model=gathered_text.first()
                    )
                )
                if _verify_route(current_routes[-1]) != False:
                    found_route.append(current_routes[-1])
                    return current_routes[-1]
            else: 
                current_routes.append(
                    Route(
                        name=pattern.name,
                        route_type="main"
                    )
                )
                if _verify_route(current_routes[-1]) != False:
                    found_route.append(current_routes[-1])
                    return current_routes[-1]
                
    def _verify_route(current_route):
        """
        Check if a given route matches the request path
        """
        current_checking_route = current_route
        if app == 'panel':
            if current_checking_route.route_type == 'main' or current_checking_route.route_type == 'main_with_text':
                current_checking_route.name = f'panel/{current_checking_route.name}'
                
        if (str(current_checking_route.name) == str(request_path)
        or str(f'{current_checking_route.name}/') == str(request_path)):
            return True
       
        return False
    
    # Begin route check      
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
    first_slash = request.path.index('/')
    request_path = request.path[:first_slash]+request.path[first_slash+1:]
    
    # Get Site Avatar URL if possible, use no user image if unavailable
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
    found_route: list = []
    
    # Check routes from Django URLPatterns
    main_routes = _get_main_routes()
    if len(found_route) > 0:
            
        if main_routes.name == 'main_with_text':
            return {
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{request_path}",
                "og_image": f"{site_avatar_url}",
                "og_title": f"{site_info.brand_name} | {request_path.title()}",
                "og_desc": strip_tags(main_routes.model.content)
            }
        
        return {
            "og_color": site_info.main_color,
            "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{request_path}",
            "og_image": f"{site_avatar_url}",
            "og_title": f"{site_info.brand_name} | {request_path.title()}",
            "og_desc": site_info.meta_description
        }
    
    # Check routes from models with defined routes
    model_routes = _get_models_routes()
    if len(found_route) > 0:
        
        if model_routes.route_type == 'user':
            try:
                user_avatar =  f"{WEB_PROTO}://{DOMAIN_NAME}{model_routes.model.user_profile_info.profile_picture.url}"
            except ValueError:
                user_avatar = site_avatar_url
                
            return {
                "og_user": model_routes.model,
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{BASE_USER_URL}/{model_routes.model.user_slug}",
                "og_image": f"{user_avatar}",
                "og_title": f"{site_info.brand_name} | {model_routes.model.username}",
                "og_desc": f"User Profile for {model_routes.model.username}"
            }
            
        if model_routes.route_type == 'page':
            return {
                "og_page": model_routes.model,
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/{model_routes.model.get_absolute_url()}",
                "og_image": f"{site_avatar_url}",
                "og_title": f"{site_info.brand_name} | {model_routes.model.name}",
                "og_desc": model_routes.model.meta_description
            }
            
        if model_routes.route_type == 'server':
            return {
                "og_server": model_routes.model,
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/onboarding/{slugify(model_routes.model.modpack_name)}",
                "og_image": f"{site_avatar_url}",
                "og_title": f"{site_info.brand_name} | {model_routes.model.modpack_name} Onboarding",
                "og_desc": strip_tags(model_routes.model.modpack_description)
            }
            
        if model_routes.route_type == 'donationpackage':
            return {
                "og_package": model_routes.model,
                "og_color": site_info.main_color,
                "og_url": f"{WEB_PROTO}://{DOMAIN_NAME}/donations/checkout{slugify(model_routes.model.pk)}",
                "og_image": f"{site_avatar_url}",
                "og_title": f"{site_info.brand_name} | {model_routes.model.name}",
                "og_desc": strip_tags(model_routes.model.package_description)
            }
            
        return True
    
    return False
    