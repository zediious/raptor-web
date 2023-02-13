from typing import Optional

from django import template

from raptorWeb.gameservers.models import Server

register: template.Library = template.Library()

@register.filter
def get_key(value: str) -> str:
    """
    Get key from server address
    """
    return value.split('.')[0]
