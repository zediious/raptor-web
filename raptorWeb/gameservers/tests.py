from django.test import TestCase

from raptorWeb.gameservers.models import Server
from raptorWeb.gameservers.util.playerCounts import PlayerCounts

class ServerTestCase(TestCase):
    def setUp(self):
        Server.objects.create()

        Server.objects.create(
            server_state = True,
            in_maintenance = True,
            server_address = 'hypixel.net',
            server_port = 25565,
            modpack_name = "Vanilla",
            modpack_version = '1.18/1.19',
            modpack_description = "This is a vanilla minecraft server",
            server_description = "This server has little features",
            server_rules = "There are no specific rules",
            server_banned_items = "There are no banned items",
            server_vote_links = "Vote links are not available",
            modpack_url = "https://hypixel.net/",
        )

    def test_server_info(self):
        empty_server = Server.objects.get(modpack_name='Unnamed Modpack')
        non_empty_server = Server.objects.get(modpack_name = "Vanilla")
        
        modpack_info = f'{empty_server.modpack_name}\n{non_empty_server.server_address}\n{non_empty_server.modpack_description}'

    def test_server_query(self):
        poller = PlayerCounts()
        non_empty_server = Server.objects.get(modpack_name = "Vanilla")

        poller.server_data.update({
                f"server": {
                    "address": non_empty_server.server_address,
                    "port": non_empty_server.server_port,
                    "do_query": True,
                    "is_default": False
                }
            })

        polled_data = poller.get_current_players()

