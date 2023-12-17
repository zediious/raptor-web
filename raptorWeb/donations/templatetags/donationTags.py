from logging import getLogger

from django import template
from django.utils.text import slugify
from django.conf import settings

LOGGER = getLogger('donations.donationTags')
register = template.Library()

DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
BASE_USER_URL_NUM: int = (len(BASE_USER_URL) + 1)


@register.filter
def get_package_from_url(value: str) -> str:
    """
    Get a package from main application's checkout path, and return only
    the package from that path.
    """
    return slugify(value[37:].replace('/', ''))
