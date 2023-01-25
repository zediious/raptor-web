from django.db import models
from django.contrib.auth.models import User

from raptorWeb.authprofiles.managers import DiscordAuthManager

class DiscordUserInfo(models.Model):
    """
    A User that was registered using Discord OAuth2.
    """
    objects = DiscordAuthManager()

    id = models.BigIntegerField(
        primary_key=True)

    tag = models.CharField(
        max_length=100)

    username = models.CharField(
        default="Default",
        max_length=100)    

    profile_picture = models.CharField(
        max_length=100
    )

    pub_flags = models.IntegerField()

    flags = models.IntegerField()

    locale = models.CharField(
        max_length=100
    )

    mfa_enabled = models.BooleanField()

    date_joined = models.DateTimeField(
        null=True
    )

    last_login = models.DateTimeField(
        null=True
    )

    minecraft_username = models.CharField(
        max_length=50,
        blank=True
    )

    favorite_modpack = models.CharField(
        max_length=80, 
        blank=True
    )

    def is_authenticated(self):
        return True

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "User - Discord OAuth"
        verbose_name_plural = "Users - Discord OAuth"

class UserProfileInfo(models.Model):
    """
    A User that was created with the website's registration
    form. Has a OneToOne relationship with a Django User
    """
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE)

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
        try:
            return self.user.username
        except:
            return self.discord_info.tag

    class Meta:
        verbose_name = "User - Extra Information"
        verbose_name_plural = "Users - Extra Information"
