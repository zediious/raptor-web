from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

class UserProfileInfo(models.Model):
    """
    Extra User profile information
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE)

    profile_picture = models.ImageField(
        upload_to='profile_pictures', 
        blank=True)

    minecraft_username = models.CharField(
        max_length=50)

    discord_username = models.CharField(
        max_length=50, 
        blank=True)

    favorite_modpack = models.CharField(
        max_length=80, 
        blank=True
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User - Extra Information"
        verbose_name_plural = "Users - Extra Information"

class Server(models.Model):
    """
    Represents a Minecraft Server
    Includes the name and online/offline state
    """
    server_name = models.CharField(
        max_length=50, 
        default="none", 
        unique=True)

    server_state = models.BooleanField(
        default=False)

    def __str__(self) -> str:
        return self.server_name

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

class ServerInformation(models.Model):
    """
    Contains descriptive elements of a Server.
    Has a OneToOne relationship with a Server
    """
    server = models.OneToOneField(
        Server, 
        on_delete=models.CASCADE)

    server_address = models.CharField(
        max_length=50)

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

    modpack_url = models.URLField(
        max_length=200, 
        verbose_name="Link to Modpack")

    def __str__(self):
        return str(
            "Server Information for: {}".format(self.server.server_name)
            )

    class Meta:
        verbose_name = "Server - Information"
        verbose_name_plural = "Servers - Information"

class InformativeText(models.Model):
    """
    Represents a general block of information 
    which is placed in the website.
    """
    name = models.CharField(
        max_length=50,
        default="Default",
        verbose_name="Content Name"
    )

    content = RichTextField(
        max_length=15000,
        default = "",
        verbose_name="Content"
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Informative Text",
        verbose_name_plural = "Informative Texts"

class AdminApplication(models.Model):
    """
    Applications for Admin
    """
    position = models.CharField(
        max_length=500, 
        verbose_name="Position applied for")

    age = models.IntegerField(
        verbose_name="Applicant age")

    time = models.CharField(
        max_length=500, 
        verbose_name="Time Zone and alottable time")

    mc_name = models.CharField(
        max_length=500, 
        verbose_name="Minecraft Username")

    discord_name = models.CharField(
        max_length=500, 
        verbose_name="Discord Username/ID")

    voice_chat = models.BooleanField(
        max_length=500, 
        verbose_name="Capable of using Voice Chat?")

    description = models.TextField(
        max_length=500, 
        verbose_name="General self-description")

    modpacks = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server modpacks/general Modded Minecraft")

    plugins = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of plugins/server mods and adaptability")

    api = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server APIs and Minecraft proxies.")

    IT_knowledge = models.TextField(
        max_length=500, 
        verbose_name="IT/Software/Networking knowledge, as well as whether one's work involves these topics.")

    linux = models.TextField(
        max_length=500, 
        verbose_name="Knowledge in Linux System Administration and CLI use.")

    ptero = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of Pterodactyl Panel")

    experience = models.TextField(
        max_length=500, 
        verbose_name="Experience on other servers")

    why_join = models.TextField(
        max_length=500, 
        verbose_name="Reasons for wanting to be staff.")

    def __str__(self):
        return str(
            "Application from: {}".format(self.discord_name)
            )

    class Meta:
        verbose_name = 'Admin Application'
        verbose_name_plural = 'Admin Applications'

class ModeratorApplication(models.Model):
    """
    Applications for Moderator
    """
    position = models.CharField(
        max_length=500, 
        verbose_name="Position applied for")

    age = models.IntegerField(
        verbose_name="Applicant age")

    time = models.CharField(
        max_length=500, 
        verbose_name="Time Zone and alottable time")

    mc_name = models.CharField(
        max_length=500, 
        verbose_name="Minecraft Username")

    discord_name = models.CharField(
        max_length=500, 
        verbose_name="Discord Username/ID")

    voice_chat = models.BooleanField(
        max_length=500, 
        verbose_name="Capable of Voice Chat?")

    contact_uppers = models.TextField(
        max_length=500, 
        verbose_name="Ability to reach higher-ups")

    description = models.TextField(
        max_length=50, 
        verbose_name="General self-description")

    modpacks = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server modpacks/general Modded Minecraft")
    
    experience = models.TextField(
        max_length=500, 
        verbose_name="Experience on other servers")

    why_join = models.TextField(
        max_length=500, 
        verbose_name="Reasons for wanting to be stff")

    def __str__(self):
        return str(
            "Application from: {}".format(self.discord_name)
            )

    class Meta:
        verbose_name = 'Moderator Application'
        verbose_name_plural = 'Moderator Applications'
