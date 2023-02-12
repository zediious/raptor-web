from django.db import models

from ckeditor.fields import RichTextField

class Server(models.Model):
    """
    Represents a Minecraft Server
    Includes all information about a server
    """
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

    modpack_description = RichTextField(
        max_length=1500,
        verbose_name="Modpack Description",
        help_text="A description of the modpack you are hosting on this server. Generally should describe the gameplay of the modpack itself.",
        default="Modpack Description")

    server_description = RichTextField(
        max_length=1500, 
        verbose_name="Server Description",
        help_text="A description of the features that this particular server has.",
        default="Server Description")

    server_rules = RichTextField(
        max_length=1500,
        verbose_name="Server-Specific Rules",
        help_text="Rules that are specific to this server.",
        default="Server-specific Rules"
    )

    server_banned_items = RichTextField(
        max_length=1500,
        verbose_name="Server-specific Banned Items",
        help_text="Items that are banned from being used on this server.",
        default="Server-specific Banned Items"
    )

    server_vote_links = RichTextField(
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

class PlayerCount(models.Model):
    """
    Represents a count of players on a Minecraft Server.
    Takes a Server as a Foreign Key.
    """
    server = models.ForeignKey(
        Server, 
        default=0, 
        on_delete=models.CASCADE)
    
    player_count = models.IntegerField(
        default=0, 
        unique=False)

    def __str__(self) -> str:
        return str("Player Counts for: {}").format(self.server)

    def get_count(self):
        return self.player_count

    def get_state(self):
        return self.server_state

    class Meta:
        verbose_name = "Player Count"
        verbose_name_plural = "Player Counts"

class PlayerName(models.Model):
    """
    Represents the name of a player that is on a Minecraft Server.
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
        verbose_name = "Player Name"
        verbose_name_plural = "Player Names"
