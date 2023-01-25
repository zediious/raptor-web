from re import sub, search

from django import template
from django.utils.html import urlize
from django.conf import settings

register = template.Library()

DOMAIN_NAME = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO = getattr(settings, 'WEB_PROTO')

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
    in the Discord App if installed. Will make all
    anchor targets be "_blank" to open in new tab.
    Runs default "urlize" filter internally before
    modification
    """
    initial = sub(r'https://discord', 'discord://discord', urlize(value))
    anchor = search(r'<a href="\S+"\S+>', initial)
    if anchor:
        blank_anchor = anchor.group(0).replace('<a', '<a target="_blank"')
        anchor_end = search(r'</a>', initial)
        anchor_end_icon = anchor_end.group(0).replace('</a>', f' <img class="new_tab_icon" src="{WEB_PROTO}://{DOMAIN_NAME}/static/image/new_tab_black.svg"></a>')
        return initial.replace(anchor.group(0), blank_anchor).replace(anchor_end.group(0), anchor_end_icon)
    
    return initial
