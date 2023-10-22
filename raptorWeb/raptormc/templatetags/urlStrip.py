from logging import getLogger

from django import template

LOGGER = getLogger('raptormc.urlStrip')
register: template.Library = template.Library()


@register.filter
def strip_slash(value: str) -> str:
    """
    Strip slashes from value
    """
    first_slash = value.index('/')
    return value[:first_slash]+value[first_slash+1:]
