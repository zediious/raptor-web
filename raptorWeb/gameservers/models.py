from json import dumps, load
from io import TextIOWrapper
from time import sleep
from logging import Logger, getLogger
from typing import Optional

from django.db import models
from django.utils.timezone import localtime, now
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings

from mcstatus import JavaServer
from mcstatus.querier import QueryResponse
from django_resized import ResizedImageField

from raptorWeb.raptormc.models import SiteInformation
from raptorWeb.raptorbot.models import ServerAnnouncement, DiscordBotTasks, SentEmbedMessage

LOGGER: Logger = getLogger('gameservers.models')
IMPORT_JSON_LOCATION: str = getattr(settings, 'IMPORT_JSON_LOCATION')
SERVER_FIELDS_TO_IGNORE = [
    'player_count',
    'announcement_count',
    'server_state',
    'in_maintenance'
    'server_port',
    'server_rules',
    'server_banned_items'
    'server_vote_links'
    'discord_announcement_channel_id',
    'discord_modpack_role_id '
]


class ServerManager(models.Manager):

    class _PlayerPoller():
        """
        Object containing data structures and methods used for polling
        addresses of Server models for state and player information.

        Use the poll_servers() method to utilize this object.
        """
        _has_run: bool = False
        _is_running: bool = False

        def _query_and_update_server(self, server: 'Server', do_query: bool = True) -> None:

            def _set_offline_server(server: Server) -> None:
                server.player_count = 0
                server.server_state = False
                _update_announcement_count(server)
                server.save()

            def _update_announcement_count(server: Server) -> None:
                server.announcement_count = ServerAnnouncement.objects.filter(
                                                server=server
                                            ).count()

            all_players = Player.objects.all()
            online_players = []
            
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
                    
                    for player in serverJSON.players.names:
                        checked_player = all_players.filter(name=player).first()
                        # If a Player exists, update their information
                        if checked_player is not None:
                            online_players.append(checked_player.name)
                            checked_player.server = server
                            checked_player.online = True
                            checked_player.last_online = now()
                            checked_player.save()
                        # If not, create a new Player
                        else:
                            online_players.append(player)
                            new_player = Player.objects.create(
                                name=player,
                                server=server,
                                online=True
                            )
                            new_player.save()

                except TimeoutError:
                    _set_offline_server(server)

            else:
                _set_offline_server(server)
                
            return online_players

        def poll_servers(self, servers: list['Server'], statistic_model: 'ServerStatistic') -> None:
            site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
            
            if statistic_model.time_last_polled == None:
                statistic_model.time_last_polled = localtime()
                
            minutes_since_poll = int(str(
                (localtime() - statistic_model.time_last_polled.astimezone())
                ).split(":")[1])

            if minutes_since_poll > 1 or self._has_run == False:
                self._is_running = True
                statistic_model.total_player_count = 0
                all_online_players = []
                
                for server in servers:
                    if (server.server_address == "Default"
                    or server.in_maintenance == True
                    or site_info.enable_server_query == False):
                        self._query_and_update_server(
                            server,
                            do_query = False)

                    else:
                        online_players =  self._query_and_update_server(server)
                        all_online_players.extend(online_players)
                        PlayerCountHistoric.objects.create(
                            server=server,
                            player_count=server.player_count
                        )
                        statistic_model.total_player_count += server.player_count
                        
                # Mark players who were not queried as online, but are marked as online in the database, as offline.         
                newly_offline_players = Player.objects.filter(online=True).exclude(name__in=all_online_players)
                for player in newly_offline_players:
                    player.online = False
                    player.save()

                self._has_run = True
                statistic_model.time_last_polled = localtime()
                statistic_model.save()
                LOGGER.info("Server data has been retrieved and saved")
                self._is_running = False
    
    _player_poller: _PlayerPoller = _PlayerPoller()
    
    def update_servers(self):
        """
        Through the use of PlayerCounts, do the following;

            - Query the server_address/server_port attributes of each server
            - Save the player_count and server_state attributes of iterated server to
            the newly queried results
            - Set announcement_count class attribute to the count of ServerAnnouncements
            that exist for the server
            - Create Player models for each player that is online, with a ForeignKey to the
            server they were on.
            - Save the total count of all online players to the total_player_count attribute of
            the ServerStatistic model passed as an argument.
        """
        if self.all().count() > 0 and self._player_poller._is_running == False:
            self._player_poller.poll_servers(
                [server for server in self.filter(archived=False)],
                ServerStatistic.objects.get_or_create(name="gameservers-stat")[0]
            )
            
    def get_servers(self, wait=True):
        """
        Return a list of servers that are not archived. Will check if a query is running, and wait
        to return servers until the query is finished.
        """
        if wait:
            while self._player_poller._is_running == True:
                sleep(0.1)
        
        return self.filter(archived=False).order_by('-pk')

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
    Statistics for all added servers.
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
    A Minecraft server. Created Servers will appear on the website on all
    relevant pages, and it's domain name/port will be queried for server
    state and player information.
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
            "if server querying is disabled.")
    )

    announcement_count = models.IntegerField(
        default=0,
        verbose_name="Announcement Count",
        help_text=("The amount of announcements that were made for this server and retrieved by the Discord Bot. ")
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

    modpack_picture = ResizedImageField(
        upload_to='modpack_pictures',
        verbose_name="Modpack Image",
        help_text=("An image associated with this modpack that will be displayed on the website. The optimal size for this image is "
            "820x200, where the image is wider than it is tall, but you can use any size image."),
        blank=True,
        size=[545,130],
        quality=80,
        force_format='WEBP',
        keep_meta=False)

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
    
    rcon_address = models.CharField(
        max_length=200,
        verbose_name="RCON Connection Address",
        help_text=("The IP address used to send RCON commands to this server."),
        blank=True,
        null=True,
        default=""  
    )
    
    rcon_port = models.IntegerField(
        default=00000,
        verbose_name="RCON Connection Port",
        help_text=("The network port used to send RCON commands to this server."),
        blank=True,
        null=True
    )
    
    rcon_password = models.CharField(
        max_length=500,
        verbose_name="RCON Connection Password",
        help_text=("The password used to authenticate when sending RCON commands to this server."),
        blank=True,
        null=True,
        default=""  
    )

    def __str__(self) -> str:
        return self.modpack_name

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"

class Player(models.Model):
    """
    Players that have joined a server at some point.
    """
    server = models.ForeignKey(
        Server, 
        default=0,
        on_delete=models.PROTECT)

    name = models.CharField(
        max_length=50, 
        unique=True)
    
    online = models.BooleanField(
        default=False)
     
    last_online = models.DateTimeField(
        verbose_name="Last Online",
        auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_name(self):
        return self.name

    def get_server(self):
        return self.server

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        
        
class PlayerCountHistoric(models.Model):
    """
    The total count of players on a server at a
    specific point in time. These are created each
    time servers are queried, for each server.
    """
    server = models.ForeignKey(
        Server, 
        default=0, 
        on_delete=models.CASCADE)

    player_count = models.IntegerField(
        verbose_name="Players Online")
     
    checked_time = models.DateTimeField(
        verbose_name="Time of Query",
        auto_now_add=True)
    
    def get_player_count(self):
        return self.player_count

    def get_server(self):
        return self.server

    class Meta:
        verbose_name = "Historic Player Count"
        verbose_name_plural = "Historic Player Counts"
        
        
@receiver(pre_save, sender=Server)
def update_embeds(sender, instance, *args, **kwargs):
    """
    If certain fields of a server are modified, tell the Discord Bot
    to update sent message embeds with the new information.
    """
    try:
        previous = Server.objects.get(id=instance.id)
        
        for field in instance._meta.fields:
            field_string = str(field).replace('gameservers.Server.', '')
            if field_string not in SERVER_FIELDS_TO_IGNORE:
                if getattr(previous, field_string) != getattr(instance, field_string):
                    for message in SentEmbedMessage.objects.filter(server=previous):
                        message.changed_and_unedited = True
                        message.save()
                    tasks: DiscordBotTasks = DiscordBotTasks.objects.get_or_create(pk=1)[0]
                    tasks.update_embeds = True
                    tasks.save()
                    break
    except Server.DoesNotExist:
        pass
