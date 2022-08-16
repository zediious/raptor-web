import logging

from raptormc.util.playerCounts import PlayerCounts
from raptormc.models import Server, PlayerData

class RaptorWare:

    LOGGER = logging.getLogger(__name__)
    
    NOMI = PlayerData.objects.get(pk=1)
    E6E = PlayerData.objects.get(pk=2)
    CT2 = PlayerData.objects.get(pk=3)
    FTBUA = PlayerData.objects.get(pk=4)
    OB = PlayerData.objects.get(pk=5)
    HEXXIT = PlayerData.objects.get(pk=6)
    NETWORK = PlayerData.objects.get(pk=7)

    SERVERS = [NOMI, E6E, CT2, FTBUA, OB, HEXXIT, NETWORK]

    PLAYER_DATA = PlayerData.objects

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
         # Code to be executed for each request before
         # the view (and later middleware) are called.
        response = self.get_response(request)
        
        return response
