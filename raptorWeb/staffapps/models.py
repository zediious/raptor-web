from django.db import models

class StaffApplication(models.Model):
    """
    Applications for Staff
    """
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
        default=False,
        verbose_name="Capable of using Voice Chat?")

    description = models.TextField(
        max_length=500, 
        verbose_name="General self-description")

    modpacks = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server modpacks/general Modded Minecraft")

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

class AdminApplication(StaffApplication):
    """
    Applications for Admin
    """
    position = models.CharField(
        max_length=100,
        default="Admin"
    )
    
    plugins = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of plugins/server mods and adaptability")

    api = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of server APIs and Minecraft proxies.")

    it_knowledge = models.TextField(
        max_length=500, 
        verbose_name="IT/Software/Networking knowledge, as well as whether one's work involves these topics.")

    linux = models.TextField(
        max_length=500, 
        verbose_name="Knowledge in Linux System Administration and CLI use.")

    ptero = models.TextField(
        max_length=500, 
        verbose_name="Knowledge of Pterodactyl Panel")

    class Meta:
        verbose_name = 'Admin Application'
        verbose_name_plural = 'Admin Applications'

class ModeratorApplication(StaffApplication):
    """
    Applications for Moderator
    """

    position = models.CharField(
        max_length=100,
        default="Mod",
        editable=False
    )
    
    contact_uppers = models.TextField(
        max_length=500, 
        verbose_name="Ability to reach higher-ups")

    class Meta:
        verbose_name = 'Moderator Application'
        verbose_name_plural = 'Moderator Applications'
