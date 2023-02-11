from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.http import HttpRequest
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.text import slugify
from django.utils.timezone import localtime, now
from django.forms import ModelForm
from django.core.files import File
from django.conf import settings

from requests import Response, get, post

from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

DISCORD_APP_ID: str = getattr(settings, 'DISCORD_APP_ID')
DISCORD_APP_SECRET: str = getattr(settings, 'DISCORD_APP_SECRET'),
DISCORD_REDIRECT_URL: str = getattr(settings, 'DISCORD_REDIRECT_URL'),


class RaptorUserManager(BaseUserManager):
    """
    UserManager for RaptorUsers. Handles the creating, updating, and fetching
    of RaptorUsers.
    """
    def create_superuser(self, username: str, email: str, password: str) -> 'RaptorUser':
        """
        Return a newly created RaptorUser with is_superuser attribute to true.
        Only to be called in management commands.
        """
        superuser: RaptorUser = RaptorUser.objects.create(
            username = username,
            email = email,
            is_staff = True,
            is_superuser = True
        ) 
        superuser.set_password(password)
        return superuser
    
    def create_user(self, registration_form: ModelForm) -> 'RaptorUser':
        """
        Given a validated UserRegisterForm, create and return a 
        RaptorUser who was registered using the website form.
        """
        new_user: RaptorUser = registration_form.save()
        new_user_extra: UserProfileInfo = UserProfileInfo.objects.create()
        new_user.set_password(new_user.password)
        new_user.user_slug = slugify(new_user.username)
        new_user.user_profile_info = new_user_extra
        new_user.is_discord_user = False
        new_user_extra.save()
        new_user.save()
        return new_user

    def create_discord_user(self, discord_info: Response) -> 'RaptorUser':
        """
        Given new Discord information fetched from Discord's user 
        API, create and return RaptorUser who was registered using
        Discord OAuth2.
        """
        discord_tag: str = f'{discord_info["username"]}#{discord_info["discriminator"]}'
        avatar_url: str = f'https://cdn.discordapp.com/avatars/{discord_info["id"]}/{discord_info["avatar"]}.png'
        new_discord_info: DiscordUserInfo = DiscordUserInfo.objects.create(
            id = discord_info["id"],
            tag = discord_tag,
            pub_flags = discord_info["public_flags"],
            flags = discord_info["flags"],
            locale = discord_info["locale"],
            mfa_enabled = discord_info["mfa_enabled"],
            avatar_string = discord_info["avatar"]
        )

        new_extra_info: UserProfileInfo = UserProfileInfo.objects.create()
        self.save_image_from_url_to_profile_info(new_extra_info, avatar_url)

        # Set username to discord tag instead of just username, if a user with username exists already
        if RaptorUser.objects.filter(user_slug=slugify(discord_info["username"])).count() > 0:
            username: str = discord_tag
        else:
            username: str = discord_tag.split('#')[0]

        new_user: RaptorUser = RaptorUser.objects.create( 
            is_discord_user = True,
            username = username,
            user_slug = slugify(username),
            email = discord_info["email"],
            user_profile_info = new_extra_info,
            discord_user_info = new_discord_info
        )
        # Discord-registered RaptorUsers will never/cannot authenticate with password.
        new_user.set_unusable_password()
        new_user.save()
        return new_user

    def exchange_discord_code(self, discord_code: str) -> Response:
        """
        Given a Discord OAuth2 code pertaining to an authenticated Discord user, make a 
        request to Discord's user API and retrieve information regarding that user, and
        return the get() Response object in .json format.
        """
        data: dict = {
            "client_id": DISCORD_APP_ID,
            "client_secret": DISCORD_APP_SECRET,
            "grant_type": "authorization_code",
            "code": discord_code,
            "redirect_uri": DISCORD_REDIRECT_URL,
            "scope": "identify email guilds"
        }
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        oauth_post_response: Response = post(
            "https://discord.com/api/oauth2/token",
            data=data, headers=headers)

        return get("https://discord.com/api/v6/users/@me",
            headers={'Authorization': f'Bearer {oauth_post_response.json()["access_token"]}'
        }).json()

    def update_user_profile_details(self, profile_edit_form: ModelForm, request: HttpRequest) -> 'RaptorUser':
        """
        Given a validated UserProfileInfo ModelForm and a request, update the details for
        the request's User with the new form data, and save the user.
        """
        changed_user = RaptorUser.objects.get(username=request.user)
        user_profile_info = changed_user.user_profile_info

        if profile_edit_form.cleaned_data["minecraft_username"] != '':
            user_profile_info.minecraft_username = \
                profile_edit_form.cleaned_data["minecraft_username"]

        if profile_edit_form.cleaned_data["favorite_modpack"] != '':
            user_profile_info.favorite_modpack = \
                profile_edit_form.cleaned_data["favorite_modpack"]

        if "profile_picture" in request.FILES:
            user_profile_info.profile_picture = \
                request.FILES["profile_picture"]
            user_profile_info.profile_picture.name = \
                RaptorUser.objects.create_profile_picture_filename(changed_user.user_profile_info)
            user_profile_info.picture_changed_manually = True

        if changed_user.is_discord_user == True:
            if profile_edit_form.cleaned_data["picture_changed_manually"] == True:
                RaptorUser.objects.save_image_from_url_to_profile_info(
                    user_profile_info,
                    ('https://cdn.discordapp.com/avatars/'
                        f'{changed_user.discord_user_info.id}/'
                        f'{changed_user.discord_user_info.avatar_string}.png'))               
            user_profile_info.picture_changed_manually = False

        user_profile_info.save()
        changed_user.save()
        return changed_user

    def update_discord_user_details(self, discord_user: 'DiscordUserInfo', new_info: Response) -> 'DiscordUserInfo':
        """
        Given a RaptorUser's Discord Information and new Discord information
        fetched from Discord's user API, replace the RaptorUser's username, tag,
        and profile picture attributes if the user has not manually changed theirs
        with new fetched information.

        Will check to make sure that a non-discord RaptorUser does not exist with the new
        username. If a RaptorUser does exist, the new username will have the Discord
        user's discriminator (#1234) appended to it.
        """
        base_user = RaptorUser.objects.get(discord_user_info = discord_user)
        discord_tag = f'{new_info["username"]}#{new_info["discriminator"]}'

        if RaptorUser.objects.filter(
            user_slug=slugify(new_info["username"]),
            is_discord_user = False
            ).count() > 0:
                username = discord_tag

        else:
            username = discord_tag.split('#')[0]

        if discord_user.avatar_string != new_info["avatar"] and base_user.user_profile_info.picture_changed_manually != True:
            discord_user.avatar_string = new_info["avatar"]
            RaptorUser.objects.save_image_from_url_to_profile_info(
                user_profile_info=base_user.user_profile_info,
                url=f'https://cdn.discordapp.com/avatars/{new_info["id"]}/{new_info["avatar"]}.png'
            )

        discord_user.tag = discord_tag
        base_user.username = username
        discord_user.save()
        base_user.save()
        return discord_user

    def find_slugged_user(self, slugged_username: str) -> 'RaptorUser':
        """
        Given a username, find the user 
        associated with that username.
        Input username and found username are
        compared after slugifying both.
        """
        for saved_user in  RaptorUser.objects.all():
            if str(slugify(saved_user.username)) == slugify(slugged_username):
                return saved_user

    def save_image_from_url_to_profile_info(self, user_profile_info: 'UserProfileInfo', url: str) -> None:
        """
        Given a UserProfileInfo and an image URL, save the image at the URL to the
        profile_picture ImageField, persisting it to disk.
        """
        image_request: Request = Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'})
        temp_image: NamedTemporaryFile = NamedTemporaryFile(delete=True)
        temp_image.write(
            urlopen(image_request).read()
            )
        temp_image.flush()

        user_profile_info.profile_picture.save(
            self.create_profile_picture_filename(user_profile_info),
            File(temp_image))
        user_profile_info.save()

    def create_profile_picture_filename(self, user_profile_info: 'UserProfileInfo') -> str:
        """
        Construct a filename for a profile picture based on the
        UserProfileInfo's pk and the current timestamp.
        """
        return f"profile_picture_{user_profile_info.pk}_{ localtime(now()) }.png"


class DiscordUserInfo(models.Model):
    """
    Discord Information for a User that was registered using Discord OAuth2.
    """
    id = models.BigIntegerField(
        primary_key=True,
        help_text="Discord user's ID returned from Discord, also acts as model primary key.",
        verbose_name="ID")

    tag = models.CharField(
        max_length=100,
        help_text="Combination of Discord Username and Discriminator, separated by a # sign.",
        verbose_name="Discord Tag") 

    pub_flags = models.IntegerField(
        help_text="Public flags for this Discord user returned from Discord.",
        verbose_name="Public Flags"
    )

    flags = models.IntegerField(
        help_text="Flags for this Discord user returned from Discord.",
        verbose_name="Flags"
    )

    locale = models.CharField(
        max_length=100,
        help_text="Discord user's locale.",
        verbose_name="Locale"
    )

    mfa_enabled = models.BooleanField(
        help_text="Whether this user has multi-factor authentication enabled on their Discord account.",
        verbose_name="MFA Enabled"
    )

    avatar_string = models.CharField(
        max_length=200,
        help_text="String returned from Discord, for fetching Avatar image.",
        verbose_name="Avatar String",
        null=True
    )

    def __str__(self):
        return f'DiscordUserInfo#{self.id}'

    class Meta:
        verbose_name = "User - Discord Information"
        verbose_name_plural = "Users - Discord Information"


class UserProfileInfo(models.Model):
    """
    A User's extra profile information
    """
    picture_changed_manually = models.BooleanField(
        default=False,
        null=True,
        help_text="Indicates whether a user has manually changed their profile picture or not.",
        verbose_name="Picture has been changed manually"
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        help_text="A user's profile picture, uploaded and stored locally.",
        verbose_name="Profile Picture",
        blank=True)

    minecraft_username = models.CharField(
        max_length=50,
        help_text="A user's Minecraft Username.",
        verbose_name="Minecraft Username",
        blank=True
    )

    favorite_modpack = models.CharField(
        max_length=80,
        help_text="A user's favorite Minecraft modpack.",
        verbose_name="Favorite Modpack",
        blank=True
    )

    def __str__(self):
        return f'UserProfileInfo#{self.id}'

    class Meta:
        verbose_name = "User - Extra Information"
        verbose_name_plural = "Users - Extra Information"


class RaptorUser(AbstractUser):
    """
    A Base user. Has optional OneToOne Fields to UserProfileInfo Model
    and DiscordUserInfo Model. Inherits from default Django user.
    """
    objects = RaptorUserManager()

    password_reset_token = models.CharField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name="Password Reset Token"
    )
    
    user_slug = models.SlugField(
        null=True,
        help_text="A user's username that has been converted to a slug/URL friendly format.",
        verbose_name="User Slug"
    )
    
    is_discord_user=  models.BooleanField(
        default=False,
        help_text="Indicates whether a user registered their account using Discord.",
        verbose_name="Is a Discord User"
    )

    user_profile_info = models.OneToOneField(
        UserProfileInfo,
        null=True,
        blank=True,
        related_name='profileinfo',
        help_text="A User's extra profile information, stored in separate model.",
        verbose_name="User Profile Information",
        on_delete=models.CASCADE)

    discord_user_info = models.OneToOneField(
        DiscordUserInfo,
        null=True,
        blank=True,
        related_name='discordinfo',
        help_text="A User's Discord user information, stored in a separate model. This field will/should not be populated for users that did not register with Discord.",
        verbose_name="Discord User Information",
        on_delete=models.CASCADE)

    def get_profile_info(self):
        return self.user_profile_info

    def get_discord_info(self):
        return self.discord_user_info

    def delete(self, *args, **kwargs):
        self.user_profile_info.delete()
        self.discord_user_info.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


@receiver(post_delete, sender=RaptorUser)
def post_delete_user(sender, instance, *args, **kwargs):
    """
    Receiver to delete the UserProfileInfo and DiscordUserInfo models
    with a OneToOne relationship to a RaptorUser when the RaptorUser
    is deleted from the Django Admin interface.
    """
    if instance.user_profile_info and instance.discord_user_info:
        instance.user_profile_info.delete()
        instance.discord_user_info.delete()
    elif instance.user_profile_info and not instance.discord_user_info:
        instance.user_profile_info.delete()
    elif not instance.user_profile_info and instance.discord_user_info:
        instance.discord_user_info.delete()