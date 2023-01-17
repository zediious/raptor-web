from django.db import models

from ckeditor.fields import RichTextField

class Server(models.Model):
    """
    Represents a Minecraft Server
    Includes all information about a server
    """
    server_state = models.BooleanField(
        default=False
    )

    in_maintenance = models.BooleanField(
        default=False,
        verbose_name="Maintenance Mode"
    )

    server_address = models.CharField(
        default="Default",
        max_length=50)
        
    server_port = models.IntegerField(
        default=00000
    )

    modpack_name = models.CharField(
        max_length=100,
        verbose_name="Modpack Name",
        default="Unnamed Modpack"
    )

    modpack_version = models.CharField(
        max_length=100,
        verbose_name="Modpack Version",
        default="1.0"
    )

    modpack_description = RichTextField(
        max_length=1500,
        verbose_name="Modpack Description", 
        default="Modpack Description")

    server_description = RichTextField(
        max_length=1500, 
        verbose_name="Server Description", 
        default="Server Description")

    server_rules = RichTextField(
        max_length=1500,
        verbose_name="Server-Specific Rules",
        default="Server-specific Rules"
    )

    server_banned_items = RichTextField(
        max_length=1500,
        verbose_name="Server-specific Banned Items",
        default="Server-specific Banned Items"
    )

    server_vote_links = RichTextField(
        max_length=1500,
        verbose_name="Voting Site Links",
        default="Server-specific Vote Links"
    )

    modpack_picture = models.ImageField(
        upload_to='modpack_pictures', 
        blank=True)

    modpack_url = models.URLField(
        max_length=200, 
        verbose_name="Link to Modpack")

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
