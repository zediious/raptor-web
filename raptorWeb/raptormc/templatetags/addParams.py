from logging import getLogger

from django import template

LOGGER = getLogger('raptormc.addParams')
register = template.Library()

@register.simple_tag(takes_context=True)
def get_param(context, value):
    """
    Return the value of a GET parameter. This needs to be
    called when wanting the value of a parameter when
    iterating over them from a template.
    """
    return context['request'].GET.get(value)
