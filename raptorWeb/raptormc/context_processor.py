from django.conf import settings

from raptorWeb.raptormc.models import SiteInformation, NavbarLink, NavbarDropdown

DOMAIN_NAME = getattr(settings, 'DOMAIN_NAME')
DEFAULT_MEDIA = getattr(settings, 'DEFAULT_MEDIA')
WEB_PROTO = getattr(settings, 'WEB_PROTO')

def context_process(request):
    site_info = SiteInformation.objects.get_or_create(pk=1)[0]
    nav_links = NavbarLink.objects.all().order_by('priority')
    nav_dropdowns = NavbarDropdown.objects.all().order_by('priority')

    return {
            "pub_domain": DOMAIN_NAME,
            "web_proto": WEB_PROTO,
            "default_media": DEFAULT_MEDIA,
            "site_info_model": site_info,
            "nav_links": nav_links,
            "nav_dropdowns": nav_dropdowns
        }