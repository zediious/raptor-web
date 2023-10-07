from django import template
from django.utils.text import slugify
from django.contrib.sessions.backends.db import SessionStore

register: template.Library = template.Library()


@register.filter
def fetch_session_id(session: SessionStore, value: str) -> str:
    """
    Fetch the value of a session key
    """
    return session.get(slugify(value))

@register.filter
def get_toast_data(value: str, toast: str) -> str:
    """
    Get specified user toast data values
    """
    return value[slugify(toast)]
