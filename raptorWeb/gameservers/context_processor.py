from django.conf import settings
from django.http import HttpResponse

from raptorWeb.gameservers.models import Server

BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
BASE_DIR: str = getattr(settings, 'BASE_DIR')
ENABLE_SERVER_QUERY: bool = getattr(settings, 'ENABLE_SERVER_QUERY')
SERVER_PAGINATION_COUNT: int = getattr(settings, 'SERVER_PAGINATION_COUNT')


def server_settings_to_context(request: HttpResponse) -> dict:
    return {"server_query_enabled": ENABLE_SERVER_QUERY,
            "server_pagination_count": SERVER_PAGINATION_COUNT,
            "total_server_count": Server.objects.filter(archived=False).count()}