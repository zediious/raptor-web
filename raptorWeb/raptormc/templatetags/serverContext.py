from re import sub

from django import template
from django.utils.html import urlize

from raptormc.models import Server

register = template.Library()

SERVER_COUNT = Server.objects.count()

@register.filter
def get_key(value):
    """
    Get key from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["key"]

        except:
            continue

@register.filter
def get_state(value):
    """
    Get server state from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["state"]

        except:
            continue

@register.filter
def get_maintenance(value):
    """
    Get maintenance status from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["maintenance"]

        except:
            continue

@register.filter
def get_address(value):
    """
    Get server address from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["address"]

        except:
            continue

@register.filter
def get_player_names(value):
    """
    Get list of player names from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["names"]

        except:
            continue

@register.filter
def get_modpack_name(value):
    """
    Get modpack name from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["modpack_name"]

        except:
            continue

@register.filter
def get_modpack_desc(value):
    """
    Get modpack description from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["modpack_description"]

        except:
            continue

@register.filter
def get_server_desc(value):
    """
    Get server description from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["server_description"]

        except:
            continue

@register.filter
def get_modpack_url(value):
    """
    Get modpack page url from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["modpack"]

        except:
            continue

@register.filter
def server_rules(value):
    """
    Get server rules from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["server_rules"]

        except:
            continue

@register.filter
def server_banned_items(value):
    """
    Get server banned items from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["server_banned_items"]

        except:
            continue

@register.filter
def server_vote_links(value):
    """
    Get server vote links from context dictionary.
    """
    for number in range(0, SERVER_COUNT):

        try:
            return value[f"server{number}"]["server_vote_links"]

        except:
            continue