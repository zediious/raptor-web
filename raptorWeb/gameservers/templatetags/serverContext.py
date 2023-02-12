from typing import Optional

from django import template

from raptorWeb.gameservers.models import Server

register: template.Library = template.Library()

def find_server(server_count: int, initial_value: dict, value_to_find: str) -> Optional[str]:
    """
    Used by all serverContext filters to find nested values in context
    """
    for number in range(0, server_count):
        try:
            return initial_value[f"server{number}"][value_to_find]
        except:
            continue

@register.filter
def get_key(value: dict) -> str:
    """
    Get key from context dictionary.
    """
    return find_server(Server.objects.count(), value, "key")

@register.filter
def get_state(value: dict) -> str:
    """
    Get server state from context dictionary.
    """
    return find_server(Server.objects.count(), value, "state")

@register.filter
def get_maintenance(value: dict) -> str:
    """
    Get maintenance status from context dictionary.
    """
    return find_server(Server.objects.count(), value, "maintenance")

@register.filter
def get_address(value: dict) -> str:
    """
    Get server address from context dictionary.
    """
    return find_server(Server.objects.count(), value, "address")

@register.filter
def get_player_names(value: dict) -> str:
    """
    Get list of player names from context dictionary.
    """
    return find_server(Server.objects.count(), value, "names")

@register.filter
def get_modpack_name(value: dict) -> str:
    """
    Get modpack name from context dictionary.
    """
    return find_server(Server.objects.count(), value, "modpack_name")

@register.filter
def get_modpack_desc(value: dict) -> str:
    """
    Get modpack description from context dictionary.
    """
    return find_server(Server.objects.count(), value, "modpack_description")

@register.filter
def get_server_desc(value: dict) -> str:
    """
    Get server description from context dictionary.
    """
    return find_server(Server.objects.count(), value, "server_description")

@register.filter
def get_modpack_url(value: dict) -> str:
    """
    Get modpack page url from context dictionary.
    """
    return find_server(Server.objects.count(), value, "modpack")

@register.filter
def get_rules(value: dict) -> str:
    """
    Get server rules from context dictionary.
    """
    return find_server(Server.objects.count(), value, "server_rules")

@register.filter
def get_banned_items(value: dict) -> str:
    """
    Get server banned items from context dictionary.
    """
    return find_server(Server.objects.count(), value, "server_banned_items")

@register.filter
def get_vote_links(value: dict) -> str:
    """
    Get server vote links from context dictionary.
    """
    return find_server(Server.objects.count(), value, "server_vote_links")

@register.filter
def get_modpack_version(value: dict) -> str:
    """
    Get modpack version from context dictionary.
    """
    return find_server(Server.objects.count(), value, "modpack_version")

@register.filter
def get_player_count(value: dict) -> str:
    """
    Get a server's player count from context dictionary.
    """
    return find_server(Server.objects.count(), value, "player_count")

@register.filter
def get_announcement_count(value: dict) -> str:
    """
    Get a server's announcement count from context dictionary.
    """
    return find_server(Server.objects.count(), value, "announcement_count")

@register.filter
def get_modpack_image(value: dict) -> str:
    """
    Get a server's modpack image from context dictionary
    """
    return find_server(Server.objects.count(), value, "modpack_image")
