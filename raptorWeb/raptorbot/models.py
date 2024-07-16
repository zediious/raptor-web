from logging import Logger, getLogger

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

LOGGER: Logger = getLogger('raptorbot.models')
    
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

    message = models.TextField(
        max_length=16383,
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
    Announcements that have been made to the entire network.
    """
    def routes(self, app):
        if app == 'main':
            return None
        
        if app == 'panel':
            return ((f'panel/bot/globalannouncement/view/{self.pk}',),)
        
        return Exception('Either "app" or "main" must be passed as an argument')
            
    def route_name(self):
        return 'globalannouncement'
    
    class Meta:
        verbose_name = "Global Announcement"
        verbose_name_plural = "Global Announcements"

class ServerAnnouncement(Announcement):
    """
    Announcements that have been made for a specific Minecraft server.
    """
    server = models.ForeignKey(
        'gameservers.Server', 
        default=0, 
        on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Announcement by {self.author} for {self.server} made on {self.date.fromisoformat("2021-01-24 05:12:21.517854+00:00").strftime("%I:%M%p %d%b%Y")}'

    def get_server(self):
        return self.server
    
    def routes(self, app):
        if app == 'main':
            return None
        
        if app == 'panel':
            return ((f'panel/bot/serverannouncement/view/{self.pk}',),)
        
        return Exception('Either "app" or "main" must be passed as an argument')
            
    def route_name(self):
        return 'serverannouncement'

    class Meta:
        verbose_name = "Server Announcement"
        verbose_name_plural = "Server Announcements"

class DiscordGuild(models.Model):
        """
        The Discord Community/Guild that the Discord Bot is linked to.
        """
        guild_name = models.CharField(
             max_length=200,
            verbose_name="Guild Name",
            default="None")
        
        guild_id = models.BigIntegerField(
            verbose_name="Guild ID",
            default="None")

        invite_link = models.URLField(
            blank=True,
            verbose_name="Discord Invite Link",
            help_text="The invite link to your Discord Server. This is automatically generated by the Discord Bot"
        )
        
        total_members = models.IntegerField(
            verbose_name="Total Members",
            default="None")

        online_members = models.IntegerField(
            verbose_name="Online Members",
            default="None")

        def __str__(self) -> str:
            return self.guild_name

        def get_guild_id(self):
            return self.guild_id

        def get_total_member_count(self):
            return self.total_members

        def get_online_member_count(self):
            return self.online_members

        class Meta:
            verbose_name = "Discord Guild"
            verbose_name_plural = "Discord Guild"


class DiscordBotTasks(models.Model):
        """
        List of tasks the Discord Bot can perform.
        """
        refresh_global_announcements = models.BooleanField(
            default=False)
        
        refresh_server_announcements = models.BooleanField(
            default=False)

        update_members = models.BooleanField(
            default=False)
        
        update_embeds = models.BooleanField(
            default=False)
        
        messages_to_delete = models.TextField(
            max_length=15000,
            default="",
            blank=True,
            null=True
        )
        
        users_and_roles_to_give = models.TextField(
            max_length=15000,
            default="",
            blank=True,
            null=True
        )

        def __str__(self) -> str:
            return f'DiscordBotTasks#{self.pk}'

        class Meta:
            verbose_name = "Discord Bot Tasks"
            verbose_name_plural = "Discord Bot Tasks"
            
            
class DiscordBotInternal(models.Model):
        """
        Interal tracking information used by the application to
        control the discord bot.
        """
        name = models.CharField(
            default="botinternal-stat",
            max_length=150
        )
        
        time_last_stopped = models.DateTimeField(
            default=None,
            null=True
        )
        
        deleted_a_message = models.BooleanField(
            default=False,
            help_text=("True if the Discord Bot deletes a message. Set back to True" 
                       "after the delete receiver runs.")
        )

        def __str__(self) -> str:
            return f'DiscordBotInternal#{self.pk}'

        class Meta:
            verbose_name = "Discord Bot Internal"
            verbose_name_plural = "Discord Bot Internal"
            
            
class SentEmbedMessage(models.Model):
        """
        An embed message that has been sent by the Discord Bot
        via command from a Discord server/channel. If one of these messages
        is deleted here or in Discord, it will be deleted in the other place.
        """
        server = models.ForeignKey(
            'gameservers.Server', 
            default=0, 
            on_delete=models.PROTECT
            )
        
        webhook_id = models.CharField(
            default="",
            max_length=500
        )
        
        message_id = models.CharField(
            default="",
            max_length=500
        )
        
        channel_id = models.CharField(
            default="",
            max_length=500
        )
        
        sent = models.DateTimeField(
            verbose_name="Originally Sent",
            auto_now_add=True
        )
        
        modified = models.DateTimeField(
            verbose_name="Last Modified",
            auto_now_add=True
        )
        
        changed_and_unedited = models.BooleanField(
            verbose_name="Changed and Unedited",
            default=False
        )

        def __str__(self) -> str:
            return f'{self.server}-{self.pk}'

        class Meta:
            verbose_name = "Embed Message"
            verbose_name_plural = "Embed Messages"


@receiver(post_delete, sender=SentEmbedMessage)
def delete_embed(sender, instance, *args, **kwargs):
    """
    If a SentMessageEmbed is deleted, add the message ID
    of the SentMessageEmbed to the queue of deleted messages
    for the Bot to delete.
    """
    bot_stats = DiscordBotInternal.objects.get_or_create(name="botinternal-stat")[0]
    if bot_stats.deleted_a_message:
        bot_stats.deleted_a_message = False
        bot_stats.save()
    
    else:
        tasks: DiscordBotTasks = DiscordBotTasks.objects.get_or_create(pk=1)[0]
        if tasks.messages_to_delete == None:
            tasks.messages_to_delete = ""

        current_queue = tasks.messages_to_delete
        current_queue += f'({instance.message_id}.{instance.channel_id}),'
        tasks.messages_to_delete = current_queue
        tasks.save()
