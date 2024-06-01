from six import text_type
from os.path import join, exists
from os import makedirs
from qrcode import make
import qrcode.image.svg
from datetime import datetime
from logging import Logger, getLogger

from pyotp import random_base32, TOTP

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from raptorWeb.raptormc.models import SiteInformation

QR_MEDIA_DIR: str = join(getattr(settings, 'MEDIA_DIR'), 'totp/')
LOGGER: Logger = getLogger('authprofiles.tokens')

class RaptorUserTokenGenerator(PasswordResetTokenGenerator):
    """
    Password reset token generator used for the RaptorUser
    password reset process.
    """
    def _make_hash_value(self, user: AbstractUser, timestamp: int) -> str:
        return make_hash_value(user, timestamp)


def make_hash_value(user: AbstractUser, timestamp: int) -> str:
    """
    Return a hash value derived from a Users details and the current time
    """
    return (f'{text_type(user.pk)}'
            f'{text_type(timestamp)}'
            f'{text_type(user.is_active)}'
            f'{text_type(user.user_profile_info.favorite_modpack)}'
            f'{text_type(user.user_profile_info.minecraft_username)}'
            f'{text_type(user.date_joined)}'
            f'{text_type(user.last_login)}') 
        
def generate_totp_token(user: AbstractUser) -> str:
    """
    When a user first sets up two factor authentication, generate a token for them
    and assign it to their user. Further, save an image of the QR code for the set
    up, and return the URL path for this QR code.
    """
    site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
    user.totp_token = bytes(random_base32(), 'utf-8')
    
    if not exists(QR_MEDIA_DIR):
        makedirs(QR_MEDIA_DIR)
    
    totp = TOTP(user.totp_token)
    qr_uri = totp.provisioning_uri(
        name=f'{user.username}/{user.email}',
        issuer_name=site_info.brand_name
    )
    
    qr_filename =  f'{QR_MEDIA_DIR}{hash(datetime.now())}.svg'
    LOGGER.debug(qr_filename)

    qr_code_image = make(
        qr_uri,
        image_factory=qrcode.image.svg.SvgPathImage
    )
    
    qr_code_image.save(qr_filename)
    
    file_path = qr_filename.replace('/raptorWebApp/raptorWeb', '')
    user.totp_qr_path = file_path
    user.save()
    
    return file_path
    
def check_totp_token(user: AbstractUser, otp):

    totp = TOTP(user.totp_token)

    return totp.verify(otp)
