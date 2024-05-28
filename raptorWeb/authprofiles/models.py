from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile
from logging import Logger, getLogger

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.http import HttpRequest
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.text import slugify
from django.utils.timezone import localtime, now
from django.forms import ModelForm
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings

from requests import Response, get, post
from django_resized import ResizedImageField

from raptorWeb.authprofiles.tokens import RaptorUserTokenGenerator

LOGGER: Logger = getLogger('authprofiles.models')
DISCORD_APP_ID: str = getattr(settings, 'DISCORD_APP_ID')
DISCORD_APP_SECRET: str = getattr(settings, 'DISCORD_APP_SECRET'),
DISCORD_REDIRECT_URL: str = getattr(settings, 'DISCORD_REDIRECT_URL'),
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
USER_RESET_URL: str = getattr(settings, 'USER_RESET_URL')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
EMAIL_HOST_USER: str = getattr(settings, 'EMAIL_HOST_USER')

token_generator: RaptorUserTokenGenerator = RaptorUserTokenGenerator()


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
        superuser: RaptorUser = self.create(
            username=username,
            email=email,
            is_staff=True,
            is_superuser=True
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
        discord_tag: str = f'{discord_info["username"]}#'
        avatar_url: str = ('https://cdn.discordapp.com/avatars/'
                            f'{discord_info["id"]}/{discord_info["avatar"]}.png')

        new_discord_info: DiscordUserInfo = DiscordUserInfo.objects.create(
            id=discord_info["id"],
            tag=discord_tag.replace('#', ''),
            pub_flags=discord_info["public_flags"],
            flags=discord_info["flags"],
            locale=discord_info["locale"],
            mfa_enabled=discord_info["mfa_enabled"],
            avatar_string=discord_info["avatar"]
        )

        new_extra_info: UserProfileInfo = UserProfileInfo.objects.create()
        try:
            new_extra_info.save_profile_picture_from_url(avatar_url)
        except Exception as exception:
            LOGGER.debug((f"When creating an account for Discord user {discord_tag}, the following exception occured. "
                         f"This usually just means that the user does not have a profile picture. {exception}"))

        # Set username to discord tag instead of just username, if a user with username exists already
        if self.filter(
            user_slug=slugify(discord_info["username"])).count() > 0:
                username: str = discord_tag
        else:
            username: str = discord_tag.split('#')[0]

        new_user: RaptorUser = self.create( 
            is_discord_user=True,
            username=username,
            user_slug=slugify(username),
            email=discord_info["email"],
            user_profile_info=new_extra_info,
            discord_user_info=new_discord_info
        )
        # Discord-registered RaptorUsers will never/cannot authenticate with password.
        new_user.set_unusable_password()
        new_user.save()
        return new_user

    def send_reset_email(self, reset_form):
        """
        Given a valid password reset email sending form, send a password
        reset email to a user's email, if the user is not a Discord user.
        Return True, if an email was sent, False if not.
        """
        resetting_user: RaptorUser = self.get(
            username = reset_form.cleaned_data["username"],
            email = reset_form.cleaned_data["email"])
        if resetting_user.is_discord_user == True:
            return False

        resetting_user.password_reset_token = token_generator.make_token(resetting_user)
        resetting_user.save()
        send_mail(subject=f"User password reset for: {resetting_user.username}",
            message=("Click the following link to enter a password reset form for your account: "
                    f"{WEB_PROTO}://{DOMAIN_NAME}/"
                    f"{BASE_USER_URL}/{USER_RESET_URL}/"
                    f"{resetting_user.user_slug}/{resetting_user.password_reset_token}"),
            from_email=EMAIL_HOST_USER,
            recipient_list=[resetting_user.email]
        )
        LOGGER.info(f"Password reset submitted for {resetting_user.username}. Email has been sent.")
        return True

    def exchange_discord_code(self, discord_code: str) -> Response:
        """
        Given a Discord OAuth2 code pertaining to an authenticated Discord user, make a 
        request to Discord's user API and retrieve information regarding that user, and
        return the get() Response object in .json format.
        """
        data: dict[str, str] = {
            "client_id": DISCORD_APP_ID,
            "client_secret": DISCORD_APP_SECRET,
            "grant_type": "authorization_code",
            "code": discord_code,
            "redirect_uri": DISCORD_REDIRECT_URL,
            "scope": "identify email guilds"
        }
        headers: dict[str, str] = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        oauth_post_response: Response = post(
            "https://discord.com/api/oauth2/token",
            data=data, headers=headers)

        return get("https://discord.com/api/v6/users/@me",
            headers={'Authorization': f'Bearer {oauth_post_response.json()["access_token"]}'
        }).json()

    def find_slugged_user(self, slugged_username: str) -> 'RaptorUser':
        """
        Given a username, find the user 
        associated with that username.
        Input username and found username are
        compared after slugifying both.
        """
        for saved_user in  self.all():
            if str(slugify(saved_user.username)) == slugify(slugged_username):
                return saved_user


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
        help_text="The Discord username associated with this model.",
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

    def update_discord_user_details(self, new_info: Response) -> 'DiscordUserInfo':
        """
        Given new Discord information fetched from Discord's user API, replace the 
        RaptorUser's of a DiscordUserInfo username, tag, and profile picture attributes 
        if the user has not manually changed theirs with new fetched information.

        Will check to make sure that a non-discord RaptorUser does not exist with the new
        username. If a RaptorUser does exist, the new username will have a pound sign (#)
        appended to it.
        """
        base_user: RaptorUser = RaptorUser.objects.get(discord_user_info=self)
        discord_tag: str = f'{new_info["username"]}#'

        if RaptorUser.objects.filter(
            user_slug=slugify(new_info["username"]),
            is_discord_user=False
            ).count() > 0:
                username = discord_tag

        else:
            username = discord_tag.replace('#', '')

        if (self.avatar_string != new_info["avatar"]
        and base_user.user_profile_info.picture_changed_manually != True):
            self.avatar_string = new_info["avatar"]
            base_user.user_profile_info.save_profile_picture_from_url(
                ('https://cdn.discordapp.com/avatars/'
                f'{new_info["id"]}/{new_info["avatar"]}.png')
            )

        self.tag = discord_tag.replace('#', '')
        base_user.username = username
        self.save()
        base_user.user_profile_info.save()
        base_user.save()
        return self

    def __str__(self):
        return f'DiscordUserInfo#{self.id}'

    class Meta:
        verbose_name = "User - Discord Information"
        verbose_name_plural = "Users - Discord Information"


class UserProfileInfo(models.Model):
    """
    A User's extra profile information.
    """
    picture_changed_manually = models.BooleanField(
        default=False,
        null=True,
        help_text="Indicates whether a user has manually changed their profile picture or not.",
        verbose_name="Picture has been changed manually"
    )

    profile_picture = ResizedImageField(
        upload_to='profile_pictures',
        help_text="A user's profile picture, uploaded and stored locally.",
        verbose_name="Profile Picture",
        blank=True,
        size=[150,150],
        quality=50,
        force_format='WEBP',
        keep_meta=False)

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
    
    hidden_from_public = models.BooleanField(
        default=False,
        null=True,
        help_text="Indicates whether this user appears on the user list, and whether their profile is publicly accessible.",
        verbose_name="Hidden from Public"
    )

    def update_user_profile_details(self, profile_edit_form: ModelForm, uploaded_files: dict) -> 'UserProfileInfo':
        """
        Given a validated UserProfileInfo ModelForm and dict of
        upload form files, update self attributes with new info
        from model form and uploaded files
        """
        changed_user: RaptorUser = RaptorUser.objects.get(user_profile_info=self)

        if profile_edit_form.cleaned_data["minecraft_username"] != '':
            self.minecraft_username = \
                profile_edit_form.cleaned_data["minecraft_username"]

        if profile_edit_form.cleaned_data["favorite_modpack"] != '':
            self.favorite_modpack = \
                profile_edit_form.cleaned_data["favorite_modpack"]

        if "profile_picture" in uploaded_files:
            self.profile_picture = \
                uploaded_files["profile_picture"]
            self.profile_picture.name = \
                self._create_profile_picture_filename()
            self.picture_changed_manually = True

        if (changed_user.is_discord_user == True
        and profile_edit_form.cleaned_data["picture_changed_manually"] == True):
            self.picture_changed_manually = False
            self.save_profile_picture_from_url(
                ('https://cdn.discordapp.com/avatars/'
                f'{changed_user.discord_user_info.id}/'
                f'{changed_user.discord_user_info.avatar_string}.png'))
        
        if profile_edit_form.cleaned_data["reset_toasts"] == True:
            changed_user.toasts_seen = dict()
            changed_user.save()
        
        is_hidden = profile_edit_form.cleaned_data["hidden_from_public"]
        if is_hidden != self.hidden_from_public:
            self.hidden_from_public = is_hidden        

        self.save()
        return self
    
    def save_profile_picture_from_url(self, url: str) -> None:
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

        self.profile_picture.save(
            self._create_profile_picture_filename(),
            File(temp_image))
        self.save()

    def _create_profile_picture_filename(self) -> str:
        """
        Construct a filename for a profile picture based on the
        UserProfileInfo's pk and the current timestamp.
        """
        return f"profile_picture_{self.pk}_{ localtime(now()) }.png"

    def __str__(self):
        return f'UserProfileInfo#{self.id}'

    class Meta:
        verbose_name = "User - Extra Information"
        verbose_name_plural = "Users - Extra Information"


class RaptorUser(AbstractUser):
    """
    A User on the website. Has optional OneToOne Fields to UserProfileInfo Model
    and DiscordUserInfo Model, which store extra information about the user.

    Users can be registered with the website using a form, or they can register
    using Discord OAuth2. If a User registers with the latter, they will not be
    able to log into their account using a password, and their password field will
    be rendered unuseable.
    """
    objects = RaptorUserManager()

    date_queued_for_delete = models.DateTimeField(
        verbose_name="Date Queued for Deletion",
        default=None,
        blank=True,
        null=True
    )

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
    
    toasts_seen = models.JSONField(
        default=dict,
        help_text="JSON data representing which Notification Toasts this user has seen",
        verbose_name="Seen Notifications",
        blank=True,
        null=True
    )

    def get_profile_info(self):
        return self.user_profile_info

    def get_discord_info(self):
        return self.discord_user_info

    def get_absolute_url(self):
        return f"/{BASE_USER_URL}/{self.user_slug}"

    def delete(self, *args, **kwargs): 
        """
        Delete associated UserProfileInfo and DiscordUserInfo
        models associated with a deleted RaptorUser.
        """
        if self.user_profile_info and self.discord_user_info:
            self.user_profile_info.delete()
            self.discord_user_info.delete()
            
        elif self.user_profile_info and not self.discord_user_info:
            self.user_profile_info.delete()
            
        elif not self.user_profile_info and self.discord_user_info:
            self.discord_user_info.delete()
            
        return super(self.__class__, self).delete(*args, **kwargs)
    
    
class RaptorUserGroup(Group):
    """
    A group for assigning permissions to RaptorUsers. Extends Django's default group
    """
    class Meta:
        verbose_name = "Permission Group"
        verbose_name_plural = "Permission Groups"
    

class DeletionQueueForUser(models.Model):
    """
    A list of users who have requested account deletion.
    """
    user = models.ForeignKey(
        RaptorUser, 
        on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Users Queued for Deletion"
        verbose_name_plural = "Users Queued for Deletion"
