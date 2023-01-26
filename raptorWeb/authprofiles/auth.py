from logging import getLogger
from random import randint

from django.contrib.auth.backends import BaseBackend
from django.core.files.base import ContentFile

from requests import get

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo, DiscordUserInfo

LOGGER = getLogger('raptorWeb.authprofiles.auth')

class DiscordAuthBackend(BaseBackend):

    def authenticate(self, request, user):
        try:
            find_user = RaptorUser.objects.get(username=f'{user["username"]}#{user["discriminator"]}')
            return find_user
        except RaptorUser.DoesNotExist:
            LOGGER.info("No user found with Username, creating now")
            discord_tag = f'{user["username"]}#{user["discriminator"]}'
            avatar_url = f'https://cdn.discordapp.com/avatars/{user["id"]}/{user["avatar"]}.png'
            avatar_image = ContentFile(get(avatar_url).content)

            new_discord_info = DiscordUserInfo.objects.create(
                id = user["id"],
                tag = discord_tag,
                pub_flags = user["public_flags"],
                flags = user["flags"],
                locale = user["locale"],
                mfa_enabled = user["mfa_enabled"],
            )

            new_extra_info = UserProfileInfo.objects.create(
                profile_picture = avatar_image
            )

            new_user = RaptorUser.objects.create(
                is_discord_user = True,
                username = discord_tag.split('#')[0],
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
