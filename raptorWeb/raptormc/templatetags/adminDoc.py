from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.simple_tag()
def get_admin_documentation(obj):
    if obj.__doc__:
        return mark_safe(f'<p style="font-size: 20px;">{obj.__doc__}</p>')
    return ''
