from django.contrib.auth.backends import BaseBackend
from authprofiles.models import DiscordUserInfo

from logging import getLogger

LOGGER = getLogger('authprofiles.auth')

class DiscordAuthBackend(BaseBackend):

    def authenticate(self, request, user):
        find_user = DiscordUserInfo.objects.filter(id=user["id"])
        if len(find_user) == 0:
            LOGGER.info("No user found with Discord ID, creating now")
            new_user = DiscordUserInfo.objects.create_new_discord_user(user)
            return new_user

        elif len(find_user) == 1:
            LOGGER.debug(find_user.first())
            return find_user

    def get_user(self, user_id):

        try:
            return DiscordUserInfo.objects.get(pk=user_id)
        except DiscordUserInfo.DoesNotExist:
            return None
