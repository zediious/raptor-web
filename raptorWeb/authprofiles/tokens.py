from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import AbstractUser
import six


class RaptorUserTokenGenerator(PasswordResetTokenGenerator):
    """
    Password reset token generator used for the RaptorUser
    password reset process.
    """
    def _make_hash_value(self, user: AbstractUser, timestamp: int) -> str:
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
