from logging import Logger, getLogger
from typing import Optional

from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.utils.text import slugify

from raptorWeb.authprofiles.models import RaptorUser

LOGGER: Logger = getLogger('raptorWeb.authprofiles.auth')

class DiscordAuthBackend(BaseBackend):

    def authenticate(self, request: HttpRequest, user: dict) -> RaptorUser:
        """
        Return a RaptorUser if information in Discord user API response matches a current
        RaptorUser whose is_discord_user attribute is True. If not, create a new RaptorUser
        based on the Response object data and return that new RaptorUser.
        """
        try:
            return RaptorUser.objects.get(user_slug=slugify(user["username"]), is_discord_user=True)
        except RaptorUser.DoesNotExist:
            try: 
                return RaptorUser.objects.get(user_slug=slugify(f'{user["username"]}#{user["discriminator"]}'), is_discord_user=True)
            except RaptorUser.DoesNotExist:
                LOGGER.info("No user found with Username, creating now")
                return RaptorUser.objects.create_discord_user(user)

    def get_user(self, user_id: int) -> Optional[RaptorUser]:
        """
        Get a RaptorUser whose pk matches user_id parameter.
        Return None if there is no match.
        """
        try:
            return RaptorUser.objects.get(pk=user_id, is_discord_user=True)
        except RaptorUser.DoesNotExist:
            return None
