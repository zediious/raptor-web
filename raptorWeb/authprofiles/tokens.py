from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from raptorWeb.authprofiles.models import RaptorUser

class RaptorUserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: RaptorUser, timestamp: int) -> str:
        return f'{six.text_type(user.pk)}{six.text_type(timestamp)}{six.text_type(user.is_active)}'
