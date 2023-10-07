from django.http import HttpRequest
from django.utils.text import slugify
from django.conf import settings

from raptorWeb.raptormc.models import SiteInformation, SmallSiteInformation, NavbarLink, NavbarDropdown, NavWidget, NavWidgetBar, NotificationToast, DefaultPages

DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
DEFAULT_MEDIA: str = getattr(settings, 'DEFAULT_MEDIA')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')

def context_process(request: HttpRequest) -> dict:
    default_pages: DefaultPages.objects = DefaultPages.objects.get_or_create(pk=1)[0]
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
    small_site_info: SmallSiteInformation.objects = SmallSiteInformation.objects.get_or_create(pk=1)[0]
    nav_links: NavbarLink.objects = NavbarLink.objects.filter(enabled=True).order_by('priority')
    nav_dropdowns: NavbarDropdown.objects = NavbarDropdown.objects.filter(enabled=True).order_by('priority')
    nav_widgets: NavWidget.objects = NavWidget.objects.filter(enabled=True).order_by('priority')
    nav_widget_bars: NavWidgetBar.objects = NavWidgetBar.objects.filter(enabled=True).order_by('priority')
    notification_toasts: NotificationToast.objects = NotificationToast.objects.filter(enabled=True).order_by('created')

    if (request.headers.get('HX-Request') != "true" and
        request.headers.get('Sec-Fetch-Mode') == 'navigate'):
        if not request.user.is_authenticated:
            for toast in notification_toasts:
                slugged_toast = slugify(toast.name)
                try:
                    if request.session[slugged_toast] != 2:
                        request.session[slugged_toast] = 2

                except KeyError:
                    request.session[slugged_toast] = 1

    return {
            "pub_domain": DOMAIN_NAME,
            "web_proto": WEB_PROTO,
            "default_media": DEFAULT_MEDIA,
            "default_pages": default_pages, 
            "site_info_model": site_info,
            "small_site_info": small_site_info,
            "nav_links": nav_links,
            "nav_dropdowns": nav_dropdowns,
            "nav_widgets": nav_widgets,
            "nav_widget_bars": nav_widget_bars,
            "notification_toasts": notification_toasts
        }