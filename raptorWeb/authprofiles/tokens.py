from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from raptorWeb.authprofiles.models import RaptorUser


class RaptorUserTokenGenerator(PasswordResetTokenGenerator):
    """
    Password reset token generator used for the RaptorUser
    password reset process.
    """
    def _make_hash_value(self, user: RaptorUser, timestamp: int) -> str:
        """
        Return a hash value derived from a RaptorUser's pk,
        """
        return (f'{six.text_type(user.pk)}'
                f'{six.text_type(timestamp)}'
                f'{six.text_type(user.is_active)}'
                f'{six.text_type(user.user_profile_info.favorite_modpack)}'
                f'{six.text_type(user.user_profile_info.minecraft_username)}'
                f'{six.text_type(user.date_joined)}'
                f'{six.text_type(user.last_login)}')
