from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.simple_tag()
def get_admin_documentation(obj):
    if obj.__doc__:
        return mark_safe(obj.__doc__)
    return ''

@register.simple_tag()
def get_verbose_name(obj):
    if obj._meta.verbose_name:
        if type(obj._meta.verbose_name) == tuple:
            return obj._meta.verbose_name[0]
        return obj._meta.verbose_name
    return ''
