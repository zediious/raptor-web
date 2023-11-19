from logging import getLogger

from django import template
from django.conf import settings

LOGGER = getLogger('gameservers.serverTags')
register = template.Library()

@register.filter
def get_server_from_url(value: str) -> str:
    """
    Get a server from main application's onboarding path, and 
    return only the onboarding path for the server.
    """
    return value[19:]
