from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

class DiscordUserInfo(models.Model):
    """
    Discord Information for a User that was registered using Discord OAuth2.
    """
    id = models.BigIntegerField(
        primary_key=True)

    tag = models.CharField(
        max_length=100) 

    pub_flags = models.IntegerField()

    flags = models.IntegerField()

    locale = models.CharField(
        max_length=100
    )

    mfa_enabled = models.BooleanField()

    def is_authenticated(self):
        return True

    def __str__(self):
        return f'DiscordUserInfo#{self.id}'

    class Meta:
        verbose_name = "User - Discord Information"
        verbose_name_plural = "Users - Discord Information"

class UserProfileInfo(models.Model):
    """
    A User's extra profile information
    """
    profile_picture = models.ImageField(
        upload_to='profile_pictures', 
        blank=True)

    minecraft_username = models.CharField(
        max_length=50,
        blank=True
    )

    favorite_modpack = models.CharField(
        max_length=80, 
        blank=True
    )
    def __str__(self):
        return f'UserProfileInfo#{self.id}'

    class Meta:
        verbose_name = "User - Extra Information"
        verbose_name_plural = "Users - Extra Information"

class RaptorUser(User):
    """
    A Base user. Has optional OneToOne Fields to UserProfileInfo Model
    and DiscordUserInfo Model. Inherits from default Django user.
    """
    is_discord_user=  models.BooleanField(
        blank=True,
        null=True
    )

    user_profile_info = models.OneToOneField(
        UserProfileInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    discord_user_info = models.OneToOneField(
        DiscordUserInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.user_profile_info.delete()
        self.discord_user_info.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

@receiver(post_delete, sender=RaptorUser)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user_profile_info and instance.discord_user_info:
        instance.user_profile_info.delete()
        instance.discord_user_info.delete()
    elif instance.user_profile_info and not instance.discord_user_info:
        instance.user_profile_info.delete()
    elif not instance.user_profile_info and instance.discord_user_info:
        instance.discord_user_info.delete()