from django import template
from django.utils.text import slugify
from django.conf import settings

register = template.Library()

DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
BASE_USER_URL_NUM: int = (len(BASE_USER_URL) + 1)


@register.filter
def get_user_from_url(value: str) -> str:
    """
    Get a user from main application's user path, and return only
    the username from that path.
    """
    return slugify(value[BASE_USER_URL_NUM:].replace('/', ''))
