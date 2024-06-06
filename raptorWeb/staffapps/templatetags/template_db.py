from logging import getLogger
from json import loads

from django import template

LOGGER = getLogger('staffapps.template_db')
register = template.Library()

@register.filter
def filter_in_template(object, order_by):
    return object.order_by(order_by)

@register.filter
def add_underscore(string):
    return string.replace(' ', '_')

@register.filter
def remove_underscore(string):
    return string.replace('_', ' ')

@register.filter
def json_to_dict(json_object):
    return loads(json_object)

@register.filter
def get_dict_value(dict, value):
    """
    Return the value of a dictionary key
    """
    return dict[value]
