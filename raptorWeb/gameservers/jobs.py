from os.path import join, getmtime
from logging import getLogger
from time import time
from json import dumps, load

from django.utils.html import strip_tags

from raptorWeb import settings
from gameservers.models import Server, PlayerCount, PlayerName
from gameservers.util.playerCounts import PlayerCounts

LOGGER = getLogger('raptormc.jobs')
player_poller = PlayerCounts()

class ServerWare:
    """
    Handle tasks regarding the gameservers app
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        export_server_data()

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before
        the view (and later middleware) are called.
        """
        response = self.get_response(request)

        export_server_data()
        
        return response

def update_context():
    """
    Update view context with new information
    Will only run if created .LOCK file hasn't been written to in 2 minutes.
    """
    try:

        lock_time = time() - getmtime(join(settings.BASE_DIR, 'playerCounts.LOCK'))
        if lock_time >= 120:

            refresh_server_data()

    except FileNotFoundError as e:

        LOGGER.error(e)
        LOGGER.error("playerCounts.LOCK file not present. Please create the file at the above path.")

def refresh_server_data():
    """
    Query addresses provided in all Server objects and add PlayerName and 
    PlayerCount objects to the database with a foreign key for each Server and
    update instanced PlayerCount class attribute playerPoller_DB with updated data
    """
    if settings.ENABLE_SERVER_QUERY and Server.objects.count() > 0:

        # Retrieve all Server Models from database, and update server_data class attribute with retreived data
        server_data = Server.objects.all()
        server_key = 0
        for server in server_data:

            if server.server_address == "Default":

                LOGGER.error("A server(s) exist, however they still have the default address set.")
                break

            player_poller.server_data.update({
                f"server{server_key}": {
                    "address": server.server_address,
                    "port": server.server_port
                }
            })
            server_key += 1
        
        # Use player_poller to query addresses from provided Server Models, and return gathered data
        player_data = player_poller.get_current_players()

        # Add total player count to currentPlayers_DB
        player_poller.currentPlayers_DB.update({
            "totalCount": player_data["totalCount"]
        })
        # Create PlayerName and PlayerCount objects from gathered server data after deleting previous entries
        PlayerCount.objects.all().delete()
        PlayerName.objects.all().delete()
        player_poller.currentPlayers_DB["server_info"] = []
        server_number = 0
        for key in player_data:

            if key == "totalCount":
                continue
            
            for player in player_data[key]["names"]:

                PlayerName.objects.create(server=Server.objects.get(server_address=player_data[key]["address"]), name=player).save()

            PlayerCount.objects.create(server=Server.objects.get(server_address=player_data[key]["address"]), player_count=player_data[key]["count"]).save()
            server_info = Server.objects.get(server_address=player_data[key]["address"])

            # Add announcements specific to each server gathered from JSON
            announcement_dict = {}
            do_announcement = False
            try:
                with open(join(settings.BASE_DIR, 'server_announcements.json'), "r+") as announcement_json:
                    announcement_dict = load(announcement_json)
                    if announcement_dict != {}:
                        do_announcement = True
            except Exception as e:
                LOGGER.info('server_announcements.json not present, allow Discord Bot to create and populate this file')
                do_announcement = False
            announcements = []
            if do_announcement == True:
                try:
                    for message in announcement_dict[key]:
                        announcements.append({
                            message: {
                                "author": announcement_dict[key][message]["author"],
                                "message": announcement_dict[key][message]["message"],
                                "date": announcement_dict[key][message]["date"]
                            }
                        })
                except KeyError as e:
                    LOGGER.info("A Server exists, however no announcements have been made regarding it yet. Skipping.")

            # Finalize currentPlayers_DB with updated information for current iterated server
            player_poller.currentPlayers_DB["server_info"].append({
                f"server{server_number}": {
                    "key": key,
                    "state": player_data[key]["online"],
                    "maintenance": server_info.in_maintenance,
                    "player_count": player_data[key]["count"],
                    "address": server_info.server_address,
                    "names": PlayerName.objects.all().filter(server=Server.objects.get(server_address=player_data[key]["address"])),
                    "modpack_name": server_info.modpack_name,
                    "modpack_version": server_info.modpack_version,
                    "modpack_description": server_info.modpack_description,
                    "server_description": server_info.server_description,
                    "modpack": server_info.modpack_url,
                    "announcements": announcements,
                    "announcement_count": len(announcements),
                    "server_rules": server_info.server_rules,
                    "server_banned_items": server_info.server_banned_items,
                    "server_vote_links": server_info.server_vote_links
                }
            })

            server_number += 1

        LOGGER.info("Server data has been retrieved and saved")

def export_server_data():
    """
    Export certain details from current Server Models to a json file
    """
    current_servers = {}
    server_num = 0

    for server in Server.objects.all():

        current_servers.update({
            f'server{server_num}': {
                "address": server.server_address,
                "modpack_name": server.modpack_name,
                "modpack_version": server.modpack_version,
                "modpack_description": strip_tags(server.modpack_description).replace('&gt;', '>').replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'"),
                "server_description": strip_tags(server.server_description).replace('&gt;', '>').replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'").replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'"),
                "modpack_url": server.modpack_url
            }
        })
        server_num += 1

    server_json = open(join(settings.BASE_DIR, 'server_data.json'), "w")
    server_json.write(dumps(current_servers, indent=4))
    server_json.close()
