from logging import getLogger

from raptorWeb import settings
from authprofiles.util import usergather

LOGGER = getLogger('authprofiles.userlist')
user_gatherer = usergather.UserGatherer()

class ProfileManager:
    """
    Middleware containing code to run on first initilization, as well as code to
    run whenever a request is made, before the view is displayed.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        user_gatherer.update_all_users()
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)
        return response