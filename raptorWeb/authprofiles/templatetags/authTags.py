from django import template
from django.conf import settings

register = template.Library()

DOMAIN_NAME = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO = getattr(settings, 'WEB_PROTO')
BASE_USER_URL = getattr(settings, 'BASE_USER_URL')
BASE_USER_URL_NUM = (len(BASE_USER_URL) + 1)

@register.filter
def get_user_from_url(value):
    """
    Get's a user from main applications user path, and returns only the username
    """
    return value[BASE_USER_URL_NUM:]
