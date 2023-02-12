from django.conf import settings
from django.http import HttpResponse

BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
BASE_DIR: str = getattr(settings, 'BASE_DIR')
ENABLE_SERVER_QUERY: bool = getattr(settings, 'ENABLE_SERVER_QUERY')


def server_settings_to_context(request: HttpResponse) -> dict:
    return {"server_query_enabled": ENABLE_SERVER_QUERY}