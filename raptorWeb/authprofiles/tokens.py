from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class RaptorUserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{six.text_type(user.pk)}{six.text_type(timestamp)}{six.text_type(user.is_active)}'
