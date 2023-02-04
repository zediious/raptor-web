from logging import getLogger
from random import randint

from django.contrib.auth.backends import BaseBackend
from django.core.files import File
from django.utils.text import slugify
from django.utils.timezone import localtime, now

from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo

LOGGER = getLogger('raptorWeb.authprofiles.auth')
def save_image_from_url_to_profile_info(model, url):
    image_request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    temp_image = NamedTemporaryFile(delete=True)
    temp_image.write(urlopen(image_request).read())
    temp_image.flush()
    model.profile_picture.save(f"profile_picture_{model.pk}_{localtime(now())}.png", File(temp_image))
    model.save()

class DiscordAuthBackend(BaseBackend):

    def authenticate(self, request, user):
        try:
            find_user = RaptorUser.objects.get(user_slug=slugify(user["username"]))
            return find_user
        except RaptorUser.DoesNotExist:
            LOGGER.info("No user found with Username, creating now")
            discord_tag = f'{user["username"]}#{user["discriminator"]}'
            avatar_url = f'https://cdn.discordapp.com/avatars/{user["id"]}/{user["avatar"]}.png'

            new_discord_info = DiscordUserInfo.objects.create(
                id = user["id"],
                tag = discord_tag,
                pub_flags = user["public_flags"],
                flags = user["flags"],
                locale = user["locale"],
                mfa_enabled = user["mfa_enabled"],
            )

            new_extra_info = UserProfileInfo.objects.create()
            save_image_from_url_to_profile_info(new_extra_info, avatar_url)

            username = discord_tag.split('#')[0]
            new_user = RaptorUser.objects.create( 
                is_discord_user = True,
                username = username,
                user_slug = slugify(username),
                password = randint(100000000, 999999999),
                user_profile_info = new_extra_info,
                discord_user_info = new_discord_info
            )
            return new_user


    def get_user(self, user_id):

        try:
            return DiscordUserInfo.objects.get(pk=user_id)
        except DiscordUserInfo.DoesNotExist:
            return None
