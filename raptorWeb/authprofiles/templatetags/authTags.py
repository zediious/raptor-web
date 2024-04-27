from logging import getLogger

from django import template
from django.utils.text import slugify
from django.conf import settings

LOGGER = getLogger('authprofiles.authTags')
register = template.Library()


@register.filter
def get_user_from_url(value: str) -> str:
    """
    Get a user from main application's user path, and return only
    the username from that path.
    """
    return slugify(value[23:].replace('/', ''))
