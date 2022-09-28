from re import sub

from django import template
from django.utils.html import urlize

register = template.Library()

@register.filter
def strip_markdown(value):
    """
    Removes all instances of markdown format
    from a given string.
    """
    return value.replace('_ _', '').replace('`', '').replace('**', '').replace('~~', '').replace('__', '').replace('@everyone', '').replace('▬', '').replace('.gg', '.com')

@register.filter
def strip_discord(value):
    """
    Removes all instances of unformatted Discord
    usernames and channels from a given string
    """
    updatedValue = sub(r'<[@, &, #]+\S+>', '', value)

    return updatedValue

@register.filter
def https_to_discord(value):
    """
    Changes instances of "https://discord" to 
    "discord://discord" to force the link to open
    in the Discord App if installed.
    Runs default "urlize" filter internally before
    modification
    """
    return sub(r'https://discord', 'discord://discord', urlize(value))
