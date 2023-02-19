from django.http import HttpRequest
from django.conf import settings

from raptorWeb.raptormc.models import SiteInformation, NavbarLink, NavbarDropdown

DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
DEFAULT_MEDIA: str = getattr(settings, 'DEFAULT_MEDIA')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')

def context_process(request: HttpRequest) -> dict:
    site_info = SiteInformation.objects.get_or_create(pk=1)[0]
    nav_links = NavbarLink.objects.filter(enabled=True).order_by('priority')
    nav_dropdowns = NavbarDropdown.objects.filter(enabled=True).order_by('priority')

    return {
            "pub_domain": DOMAIN_NAME,
            "web_proto": WEB_PROTO,
            "default_media": DEFAULT_MEDIA,
            "site_info_model": site_info,
            "nav_links": nav_links,
            "nav_dropdowns": nav_dropdowns
        }