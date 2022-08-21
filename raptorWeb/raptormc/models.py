from django.db import models

class Server(models.Model):
    """
    Represents a Minecraft Server
    """
    server_name = models.CharField(max_length=50, default="none", unique=True)

    server_state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.server_name

class PlayerCount(models.Model):
    """
    Represents a count of players on a Minecraft Server.
    Takes a Server as a Foreign Key.
    """
    server = models.ForeignKey(Server, default=0, on_delete=models.CASCADE)
    
    player_count = models.IntegerField(default=0, unique=False)

    def __str__(self) -> str:
        
        return str("Player Counts for: {}").format(self.server)

    def get_count(self):

        return self.player_count

    def get_state(self):

        return self.server_state

class PlayerName(models.Model):
    """
    Represents the name of a player that is on a Minecraft Server.
    Takes a Server as a Foreign Key.
    """
    server = models.ForeignKey(Server, default=0, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    def get_name(self):

        return self.name

    def get_server(self):

        return self.server

class AdminApplication(models.Model):
    """
    Applications for Admin
    """
    position = models.CharField(max_length=500, verbose_name="Position applied for")
    age = models.IntegerField(verbose_name="Applicant age")
    time = models.CharField(max_length=500, verbose_name="Time Zone and alottable time")
    mc_name = models.CharField(max_length=500, verbose_name="Minecraft Username")
    discord_name = models.CharField(max_length=500, verbose_name="Discord Username/ID")
    voice_chat = models.BooleanField(max_length=500, verbose_name="Capable of using Voice Chat?")
    description = models.TextField(max_length=500, verbose_name="General self-description")
    modpacks = models.TextField(max_length=500, verbose_name="Knowledge of server modpacks/general Modded Minecraft")
    plugins = models.TextField(max_length=500, verbose_name="Knowledge of plugins/server mods and adaptability")
    api = models.TextField(max_length=500, verbose_name="Knowledge of server APIs and Minecraft proxies.")
    IT_knowledge = models.TextField(max_length=500, verbose_name="IT/Software/Networking knowledge, as well as whether one's work involves these topics.")
    linux = models.TextField(max_length=500, verbose_name="Knowledge in Linux System Administration and CLI use.")
    ptero = models.TextField(max_length=500, verbose_name="Knowledge of Pterodactyl Panel")
    experience = models.TextField(max_length=500, verbose_name="Experience on other servers")
    why_join = models.TextField(max_length=500, verbose_name="Reasons for wanting to be staff.")

    def __str__(self):
        return str("Application from: {}".format(self.discord_name))

    class Meta:
        verbose_name = 'Admin Application'
        verbose_name_plural = 'Admin Applications'

class ModeratorApplication(models.Model):
    """
    Applications for Moderator
    """
    position = models.CharField(max_length=500, verbose_name="Position applied for")
    age = models.IntegerField(verbose_name="Applicant age")
    time = models.CharField(max_length=500, verbose_name="Time Zone and alottable time")
    mc_name = models.CharField(max_length=500, verbose_name="Minecraft Username")
    discord_name = models.CharField(max_length=500, verbose_name="Discord Username/ID")
    voice_chat = models.BooleanField(max_length=500, verbose_name="Capable of Voice Chat?")
    contact_uppers = models.TextField(max_length=500, verbose_name="Ability to reach higher-ups")
    description = models.TextField(max_length=50, verbose_name="General self-description")
    modpacks = models.TextField(max_length=500, verbose_name="Knowledge of server modpacks/general Modded Minecraft")
    experience = models.TextField(max_length=500, verbose_name="Experience on other servers")
    why_join = models.TextField(max_length=500, verbose_name="Reasons for wanting to be stff")

    def __str__(self):
        return str("Application from: {}".format(self.discord_name))

    class Meta:
        verbose_name = 'Moderator Application'
        verbose_name_plural = 'Moderator Applications'
