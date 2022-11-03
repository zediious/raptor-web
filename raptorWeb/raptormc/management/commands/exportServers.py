from django.core.management.base import BaseCommand, CommandError
from django.utils.html import strip_tags
from os.path import join
from json import dumps

from raptorWeb import settings
from raptormc.models import Server

class Command(BaseCommand):

    def handle(self, *args, **options):

        current_servers = {}
        server_num = 0

        for server in Server.objects.all():

            current_servers.update({
                f'server{server_num}': {
                    "address": server.server_address,
                    "modpack_name": server.modpack_name,
                    "modpack_description": strip_tags(server.modpack_description),
                    "server_description": strip_tags(server.server_description),
                    "modpack_url": server.modpack_url
                }
            })
            server_num += 1

        server_json = open(join(settings.BASE_DIR, 'server_data.json'), "w")
        server_json.write(dumps(current_servers, indent=4))
        server_json.close()