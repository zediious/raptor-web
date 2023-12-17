"""
All functions in this module are sent to the celery worker to be executed.
"""

from logging import getLogger
from time import sleep

from celery import shared_task

from raptorWeb.donations.models import CompletedDonation

LOGGER = getLogger('donations.tasks')

@shared_task
def send_server_commands(completed_donation_checkout_id: CompletedDonation):
    """
    Given a completed/paid for donation, send all commands attached to the
    bought package to all the servers attached to the bought package.
    """
    completed_donation = CompletedDonation.objects.get(
        checkout_id=completed_donation_checkout_id
    )
    
    completed_donation.send_server_commands()
    LOGGER.info((f'{completed_donation.minecraft_username} has donated '
                f'for the {completed_donation.bought_package} package'))
    
@shared_task
def resend_server_commands():
    """
    If any completed donations exist that have never sent commands to
    servers, send commands for all of those donations. This task is 
    configured to run every 5 minutes.
    """
    donations_with_no_commands_sent = CompletedDonation.objects.filter(
        sent_commands_count=0,
        completed=True
    )
    
    if donations_with_no_commands_sent.count() > 0:
        for donation in donations_with_no_commands_sent:
            donation.send_server_commands()
            sleep(3)
