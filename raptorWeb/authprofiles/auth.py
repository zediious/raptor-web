from logging import getLogger

from django.contrib.auth.backends import BaseBackend
from django.utils.text import slugify

from raptorWeb.authprofiles.models import RaptorUser

LOGGER = getLogger('raptorWeb.authprofiles.auth')

class DiscordAuthBackend(BaseBackend):

    def authenticate(self, request, user):
        try:
            find_user = RaptorUser.objects.get(user_slug=slugify(user["username"]), is_discord_user=True)
            return find_user
        except RaptorUser.DoesNotExist:
            try: 
                find_user = RaptorUser.objects.get(user_slug=slugify(f'{user["username"]}#{user["discriminator"]}'), is_discord_user=True)
                return find_user
            except RaptorUser.DoesNotExist:
                LOGGER.info("No user found with Username, creating now")
                return RaptorUser.objects.create_discord_user(user)

    def get_user(self, user_id):

        try:
            return RaptorUser.objects.get(pk=user_id, is_discord_user=True)
        except RaptorUser.DoesNotExist:
            return None
