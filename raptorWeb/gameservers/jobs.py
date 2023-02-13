from logging import Logger, getLogger

from django.conf import settings

from raptorWeb.gameservers.models import Server

LOGGER: Logger = getLogger('gameservers.jobs')
IMPORT_SERVERS: bool = getattr(settings, 'IMPORT_SERVERS')
DELETE_EXISTING: bool= getattr(settings, 'DELETE_EXISTING')

class ServerWare:
    """
    Handle tasks regarding the gameservers app
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        if IMPORT_SERVERS == True:
            Server.objects.import_server_data(delete_existing=DELETE_EXISTING)
            LOGGER.info("All servers from server_data_full.json have been imported. Please restart the server with IMPORT_SERVERS disabled.")

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        return self.get_response(request)
