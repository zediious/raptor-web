"""
All functions in this module are sent to the celery worker to be executed.
"""

from logging import getLogger
from os.path import join
from datetime import datetime
from time import sleep

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from celery import shared_task

from raptorWeb.authprofiles.models import RaptorUser, DeletionQueueForUser
from raptorWeb.raptormc.models import SiteInformation

LOGGER = getLogger('donations.tasks')
AUTH_TEMPLATE_DIR: str = getattr(settings, 'AUTH_TEMPLATE_DIR')
EMAIL_HOST_USER: str = getattr(settings, 'EMAIL_HOST_USER')

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
