from django.db import models

from raptorWeb import settings

if settings.SCRAPE_ANNOUNCEMENT:
    from gameservers.models import Server

    class Announcement(models.Model):
        """
        Represents an announcement.
        """
        author = models.CharField(
            max_length=100,
            verbose_name="Author",
            default="None")

        date = models.DateField(
            verbose_name="Date",
            default="None")

        message = models.CharField(
            max_length=50000,
            verbose_name="Message",
            default="None")

        def __str__(self) -> str:
            return f'Announcment by {self.author} made on {self.date}'

        def get_author(self):
            return self.author

        def get_date(self):
            return self.date

        def get_message(self):
            return self.message

        class Meta:
            verbose_name = "Announcement"
            verbose_name_plural = "Announcements"

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
            return f'Announcment by {self.author} for {self.server} made on {self.date}'

        def get_server(self):
            return self.server

        class Meta:
            verbose_name = "Server Announcement"
            verbose_name_plural = "Server Announcements"

class DiscordMemberCount(models.Model):
        """
        Represents a count of members on linked 
        Discord Community.
        """
        total_members = models.CharField(
            max_length=100,
            verbose_name="Author",
            default="None")

        online_members = models.DateField(
            verbose_name="Date",
            default="None")

        def __str__(self) -> str:
            return f'Discord Members: {self.online_members}/{self.total_members} online'

        def get_total_member_count(self):
            return self.total_members

        def get_online_member_count(self):
            return self.online_members

        class Meta:
            verbose_name = "Discord Member Count"
            verbose_name_plural = "Discord Member Counts"
