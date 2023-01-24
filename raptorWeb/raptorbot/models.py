from django.db import models

from raptorWeb import settings
    
class Announcement(models.Model):
    """
    Represents an abstract announcement.
    """
    author = models.CharField(
        max_length=100,
        verbose_name="Author",
        default="None")

    date = models.DateTimeField(
        verbose_name="Date",
        default="None")

    message = models.CharField(
        max_length=50000,
        verbose_name="Message",
        default="None")

    def __str__(self) -> str:
        return f'Announcement by {self.author} made on {self.date}'

    def get_author(self):
        return self.author

    def get_date(self):
        return self.date

    def get_message(self):
        return self.message

    class Meta:
        abstract = True

class GlobalAnnouncement(Announcement):
    """
    Represents a global announcement.
    """
    class Meta:
        verbose_name = "Global Announcement"
        verbose_name_plural = "Global Announcements"

if settings.SCRAPE_SERVER_ANNOUNCEMENT:
    from gameservers.models import Server
    class ServerAnnouncement(Announcement):
        """
        Represents an announcement made for a game server.
        Takes a Server as a Foreign Key.
        """
        server = models.ForeignKey(
            Server, 
            default=0, 
            on_delete=models.CASCADE)

        def __str__(self) -> str:
            return f'Announcement by {self.author} for {self.server} made on {self.date}'

        def get_server(self):
            return self.server

        class Meta:
            verbose_name = "Server Announcement"
            verbose_name_plural = "Server Announcements"

class DiscordGuild(models.Model):
        """
        Represents a Discord Community/Guild.
        """
        guild_name = models.CharField(
             max_length=200,
            verbose_name="Guild Name",
            default="None")
        
        guild_id = models.IntegerField(
            verbose_name="Guild ID",
            default="None")
        
        total_members = models.IntegerField(
            verbose_name="Total Members",
            default="None")

        online_members = models.IntegerField(
            verbose_name="Online Members",
            default="None")

        def __str__(self) -> str:
            return f'{self.online_members}/{self.total_members} Members Online'

        def get_guild_name(self):
            return self.guild_name

        def get_guild_id(self):
            return self.guild_id

        def get_total_member_count(self):
            return self.total_members

        def get_online_member_count(self):
            return self.online_members

        class Meta:
            verbose_name = "Discord Guild"
            verbose_name_plural = "Discord Guilds"
