from django import template

from re import sub

register = template.Library()

@register.filter
def strip_markdown(value):
    """
    Removes all instances of markdown format
    from a given string.
    """
    return value.replace('_ _', '').replace('`', '').replace('**', '').replace('~~', '').replace('__', '').replace('@everyone', '').replace('▬', '')

@register.filter
def strip_discord(value):
    """
    Removes all instances of unformatted Discord
    usernames and channels from a given string
    """
    updatedValue = sub(r'<[@, &, #]+\S+>', '', value)

    return updatedValue
