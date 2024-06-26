"""
All functions in this module are sent to the celery worker to be executed.
"""

from logging import getLogger
from os.path import join, getmtime
from os import listdir, remove
from datetime import datetime
import time

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from celery import shared_task

from raptorWeb.authprofiles.models import DeletionQueueForUser
from raptorWeb.raptormc.models import SiteInformation

LOGGER = getLogger('authprofiles.tasks')
AUTH_TEMPLATE_DIR: str = getattr(settings, 'AUTH_TEMPLATE_DIR')
QR_MEDIA_DIR: str = join(getattr(settings, 'MEDIA_DIR'), 'totp/')
EMAIL_HOST_USER: str = getattr(settings, 'EMAIL_HOST_USER')

@shared_task
def check_for_deletable_users():
    """
    Check if any users in the queue have been there for 30 days, and delete them if so.
    """    
    current_datetime = datetime.now()
            
    for user in DeletionQueueForUser.objects.all():
        time_since = current_datetime.astimezone() - user.user.date_queued_for_delete.astimezone()
        if time_since.total_seconds() / 60 >= 43200:
            user.user.delete()
            user.delete()

@shared_task
def check_for_deletable_qr_images():
    """
    Check if any QR code images have existed for more than an hour, and delete them if so..
    """
    epoch_time = int(time.time())
      
    for qr_image in listdir(QR_MEDIA_DIR):
        if (epoch_time - int(getmtime(join(QR_MEDIA_DIR, qr_image)))) / 60  >= 15:
            remove(join(QR_MEDIA_DIR, qr_image))

@shared_task
def send_delete_request_email(deleting_user: list):
    """
    Send email when a user requests to delete their account.
    """
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]

    email_text_string = render_to_string(
        join(AUTH_TEMPLATE_DIR, 'account_delete_request_email.txt'), {
            'deleting_user': deleting_user[0]
        }
    )
    
    email_html_string = render_to_string(
        join(AUTH_TEMPLATE_DIR, 'account_delete_request_email.html'), {
            'deleting_user': deleting_user[0]
        }
    )
    
    send_mail(
        subject=f"{site_info.brand_name} - Account Deletion Request for {deleting_user[0]}!",
        message=email_text_string,
        html_message=email_html_string,
        from_email=EMAIL_HOST_USER,
        recipient_list=[deleting_user[1]]
    )
