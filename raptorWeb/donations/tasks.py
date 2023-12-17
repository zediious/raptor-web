"""
All functions in this module are sent to the celery worker to be executed.
"""

from logging import getLogger

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
