from json import dumps, load
from io import TextIOWrapper
from logging import Logger, getLogger
from typing import Optional

from django.db import models
from django.utils.timezone import localtime
from django.conf import settings

from mcstatus import JavaServer
from mcstatus.querier import QueryResponse

from raptorWeb.raptorbot.models import ServerAnnouncement

LOGGER: Logger = getLogger('gameservers.models')
IMPORT_JSON_LOCATION: str = getattr(settings, 'IMPORT_JSON_LOCATION')
ENABLE_SERVER_QUERY: bool = getattr(settings, 'ENABLE_SERVER_QUERY')
SCRAPE_SERVER_ANNOUNCEMENT: bool = getattr(settings, 'SCRAPE_SERVER_ANNOUNCEMENT')

class ServerManager(models.Manager):

    class _PlayerPoller():
        """
        Object containing data structures and methods used for polling
        addresses of Server models for state and player information.

        Use the poll_servers() method to utilize this object.
        """
        _has_run: bool = False

        def _query_and_update_server(self, server: 'Server', do_query: bool = True) -> None:

            def _set_offline_server(server: Server) -> None:
                server.player_count = 0
                server.server_state = False
                _update_announcement_count(server)
                server.save()

            def _update_announcement_count(server: Server) -> None:
                if SCRAPE_SERVER_ANNOUNCEMENT:
                    server.announcement_count = ServerAnnouncement.objects.filter(
                                                    server=server
                                                ).count()

            if do_query == True:
                try:
                    serverJSON: QueryResponse = JavaServer(
                        server.server_address,
                        server.server_port
                        ).query()

                    server.player_count = serverJSON.players.online
                    server.server_state = True
                    _update_announcement_count(server)
                    server.save()
                    [Player.objects.create(
                        name=player,
                        server=server).save() for player in serverJSON.players.names]

                except TimeoutError:
                    _set_offline_server(server)

            else:
                _set_offline_server(server)

        def poll_servers(self, servers: list['Server'], statistic_model: 'ServerStatistic') -> None:
            if statistic_model.time_last_polled == None:
                statistic_model.time_last_polled = localtime()
            minutes_since_poll = int(str(
                (localtime() - statistic_model.time_last_polled.astimezone())
                ).split(":")[1])

            if minutes_since_poll > 1 or self._has_run == False:
                statistic_model.total_player_count = 0
                Player.objects.all().delete()

                for server in servers:
                    if (server.server_address == "Default"
                    or server.in_maintenance == True
                    or ENABLE_SERVER_QUERY == False):
                        self._query_and_update_server(
                            server,
                            do_query = False)

                    else:
                        self._query_and_update_server(server)
                        statistic_model.total_player_count += server.player_count

                self._has_run = True
                statistic_model.time_last_polled = localtime()
                statistic_model.save()
                LOGGER.info("Server data has been retrieved and saved")
    
    _player_poller: _PlayerPoller = _PlayerPoller()
    
    def update_servers(self):
        """
        Through the use of PlayerCounts, do the following;

            - Query the server_address/server_port attributes of each server
            - Save the player_count and server_state attributes of iterated server to
            the newly queried results
            - If SCRAPE_SERVER_ANNOUNCEMENT setting is True, set announcement_count class
            attribute to the count of ServerAnnouncements that exist for the server
            - Create Player models for each player that is online, with a ForeignKey to the
            server they were on.
            - Save the total count of all online players to the total_player_count attribute of
            the ServerStatistic model passed as an argument.
        """
        if self.all().count() > 0:
            self._player_poller.poll_servers(
                [server for server in self.filter(archived=False)],
                ServerStatistic.objects.get_or_create(name="gameservers-stat")[0]
            )

    def export_server_data(self) -> dict:
        """
        Export all server data for importing to a new instance
        Does not export server images
        """
        current_servers: dict = {}
        server_num: int = 0

        for server in self.all():
            current_servers.update({
                f'server{server_num}': {
                    "in_maintenance": server.in_maintenance,
                    "server_address": server.server_address,
                    "server_port": server.server_port,
                    "modpack_name": server.modpack_name,
                    "modpack_version": server.modpack_version,
                    "modpack_description": server.modpack_description,
                    "server_description": server.server_description,
                    "server_rules": server.server_rules,
                    "server_banned_items": server.server_banned_items,
                    "server_vote_links": server.server_vote_links,
                    "modpack": server.modpack_url,
                    "modpack_discord_channel": server.discord_announcement_channel_id,
                    "modpack_discord_role": server.discord_modpack_role_id
                }
            })
            server_num += 1

        server_json: TextIOWrapper = open(IMPORT_JSON_LOCATION, "w")
        server_json.write(dumps(current_servers, indent=4))
        server_json.close()
        return current_servers

    def import_server_data(self) -> Optional[bool]:
        """
        Create server objects based on an exsiting server_data_full.json
        Will delete existing servers first
        """
        try:
            with open(IMPORT_JSON_LOCATION, "r+") as import_json:
                import_json_dict = load(import_json)
                for server in import_json_dict:
                    new_server = self.create(
                        in_maintenance = import_json_dict[server]["in_maintenance"],
                        server_address = import_json_dict[server]["server_address"],
                        server_port = import_json_dict[server]["server_port"],
                        modpack_name = import_json_dict[server]["modpack_name"],
                        modpack_version = import_json_dict[server]["modpack_version"],
                        modpack_description = import_json_dict[server]["modpack_description"],
                        server_description = import_json_dict[server]["server_description"],
                        server_rules = import_json_dict[server]["server_rules"],
                        server_banned_items = import_json_dict[server]["server_banned_items"],
                        server_vote_links = import_json_dict[server]["server_vote_links"],
                        modpack_url = import_json_dict[server]["modpack"],
                        discord_announcement_channel_id = import_json_dict[server]["modpack_discord_channel"],
                        discord_modpack_role_id = import_json_dict[server]["modpack_discord_role"]
                    )
                    new_server.save()
        except FileNotFoundError:
            LOGGER.error("You attempted to import servers, but you did not place server_data_full.json in your BASE_DIR")
            return False

class ServerStatistic(models.Model):
    """
    Represents a collection of statistics for all servers.
    This model is used internally, not displayed in the Admin.
    """
    name = models.CharField(
        default="gameservers-stat",
        max_length=150
    )

    total_player_count = models.IntegerField(
        verbose_name="Total Player Count",
        default=0)

    time_last_polled = models.DateTimeField(
        default=None,
        null=True
    )

    class Meta:
        verbose_name = "Server Statistics"
        verbose_name_plural = "Server Statistics"

class Server(models.Model):
    """
    Represents a Minecraft Server
    Includes all information about a server
    """
    objects = ServerManager()

    archived = models.BooleanField(
        default=False,
        verbose_name="Archived",
        help_text="If a server is archived, it will not be displayed on the website or queried. Use this instead of deleting servers."
    )

    player_count = models.IntegerField(
        default=0,
        verbose_name="Player Count",
        help_text=("The amount of players that were on this server the last time it was queried. Will always be zero "
            "if ENABLE_SERVER_QUERY is False.")
    )

    announcement_count = models.IntegerField(
        default=0,
        verbose_name="Announcement Count",
        help_text=("The amount of announcements that were made for this server and retrieved by the Discord Bot. "
            "Only relevant if SCRAPE_SERVER_ANNOUNCEMENT is True and the Discord Bot is running..")
    )

    server_state = models.BooleanField(
        default=False,
        verbose_name="Online/Offline",
        help_text=("Indicates whether a server is online or offline, based on the status "
            "of the query to the provided Domain Name/Port. Only relevant if ENABLE_SERVER_QUERY is enabled in .env settings.")
    )

    in_maintenance = models.BooleanField(
        default=False,
        verbose_name="Maintenance Mode",
        help_text=("If this is enabled, this server will not have it's Domain Name/Port queried for player/state information, "
            "and its status indicator on the website will be replaced with a yellow 'Maintenance' indicator.")
    )

    server_address = models.CharField(
        default="Default",
        verbose_name="Server Address/Domain Name",
        help_text=("The address/domain name used to connect to your server and query it. This is used by the application to query "
            "the server, and is also displayed on the website for users to copy."),
        max_length=50)
        
    server_port = models.IntegerField(
        default=00000,
        verbose_name="Server Port",
        help_text=("The network port used to query your server by the application. This is not used on the website, "
            "it is only used to query information on the server."),
    )

    modpack_name = models.CharField(
        max_length=100,
        verbose_name="Modpack Name",
        help_text="The human-readable name of the modpack you are hosting on this server.",
        default="Unnamed Modpack"
    )

    modpack_version = models.CharField(
        max_length=100,
        verbose_name="Modpack Version",
        help_text="The version of the modpack you are hosting on this server.",
        default="1.0"
    )

    modpack_description = models.CharField(
        max_length=1500,
        verbose_name="Modpack Description",
        help_text="A description of the modpack you are hosting on this server. Generally should describe the gameplay of the modpack itself.",
        default="Modpack Description")

    server_description = models.CharField(
        max_length=1500, 
        verbose_name="Server Description",
        help_text="A description of the features that this particular server has.",
        default="Server Description")

    server_rules = models.CharField(
        max_length=1500,
        verbose_name="Server-Specific Rules",
        help_text="Rules that are specific to this server.",
        default="Server-specific Rules"
    )

    server_banned_items = models.CharField(
        max_length=1500,
        verbose_name="Server-specific Banned Items",
        help_text="Items that are banned from being used on this server.",
        default="Server-specific Banned Items"
    )

    server_vote_links = models.CharField(
        max_length=1500,
        verbose_name="Voting Site Links",
        help_text="A list of links to forum/vote listings for this server.",
        default="Server-specific Vote Links"
    )

    modpack_picture = models.ImageField(
        upload_to='modpack_pictures',
        verbose_name="Modpack Image",
        help_text=("An image associated with this modpack that will be displayed on the website. The optimal size for this image is "
            "820x200, where the image is wider than it is tall, but you can use any size image."),
        blank=True)

    modpack_url = models.URLField(
        max_length=200,
        verbose_name="Link to Modpack Page",
        help_text="A URL to the website where this modpack can be downloaded from."
    )

    discord_announcement_channel_id = models.CharField(
        max_length=200,
        verbose_name="Discord Announcement Channel ID",
        help_text="The Channel ID of the Discord Channel that will act as the Announcement channel for this server.",
        default="0"  
    )

    discord_modpack_role_id = models.CharField(
        max_length=200,
        verbose_name="Discord Modpack Role ID",
        help_text=("The Role ID of the Discord Role that will act as the 'Ping Role' for this server. "
        "When this Role is 'pinged' in the Discord Announcement Channel for this server, that message "
        "will be considered an announcement for this server."),
        default="0"  
    )

    def __str__(self) -> str:
        return self.modpack_name

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"

class Player(models.Model):
    """
    Represents a player that is on a Minecraft Server.
    Takes a Server as a Foreign Key.
    """
    server = models.ForeignKey(
        Server, 
        default=0, 
        on_delete=models.CASCADE)

    name = models.CharField(
        max_length=50, 
        unique=True)

    def __str__(self):
        return self.name
    
    def get_name(self):
        return self.name

    def get_server(self):
        return self.server

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
