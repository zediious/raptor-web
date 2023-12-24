"""
All functions in this module are sent to the celery worker to be executed.
"""

from logging import getLogger
from os.path import join
from time import sleep

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from celery import shared_task

from raptorWeb.donations.models import CompletedDonation
from raptorWeb.raptormc.models import SiteInformation

LOGGER = getLogger('donations.tasks')
DONATIONS_TEMPLATE_DIR: str = getattr(settings, 'DONATIONS_TEMPLATE_DIR')
EMAIL_HOST_USER: str = getattr(settings, 'EMAIL_HOST_USER')

@shared_task
def send_donation_email(completed_donation_checkout_id: CompletedDonation):
    """
    Given a completed/paid for donation, send an email to the email associated
    with the donating user, if the donation has a donating user.
    """
    completed_donation = CompletedDonation.objects.get(
        checkout_id=completed_donation_checkout_id
    )

    if completed_donation.donating_user != None:
        site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]
        
        email_text_string = render_to_string(
            join(DONATIONS_TEMPLATE_DIR, 'successful_email.txt'), {
                'package': completed_donation.bought_package.name,
                'donating_user': completed_donation.donating_user.username
            }
        )
        
        email_html_string = render_to_string(
            join(DONATIONS_TEMPLATE_DIR, 'successful_email.html'), {
                'package': completed_donation.bought_package.name,
                'donating_user': completed_donation.donating_user.username
            }
        )
        
        send_mail(
            subject=f"Thank you for donating to {site_info.brand_name}, {completed_donation.donating_user.username}!",
            message=email_text_string,
            html_message=email_html_string,
            from_email=EMAIL_HOST_USER,
            recipient_list=[completed_donation.donating_user.email]
        )

@shared_task
def send_server_commands(completed_donation_id: CompletedDonation):
    """
    Given a completed/paid for donation, send all commands attached to the
    bought package to all the servers attached to the bought package.
    """
    completed_donation = CompletedDonation.objects.get(
        pk=completed_donation_id
    )
    
    if completed_donation.bought_package.commands.all().count() > 0:
        completed_donation.send_server_commands()
    
@shared_task
def add_discord_bot_roles(completed_donation_id: CompletedDonation):
    """
    Given a completed/paid for donation, give all discord roles attached to the
    bought package to the Discord tag attached to the completed donation. Will
    only run if the complete donation ahs a Discord tag.
    """
    completed_donation = CompletedDonation.objects.get(
        pk=completed_donation_id
    )
    
    if completed_donation.bought_package.discord_roles.all().count() > 0:
        completed_donation.give_discord_roles()
    
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
            if donation.bought_package.commands.all().count() > 0:
                donation.send_server_commands()
                sleep(3)
            
@shared_task
def readd_discord_bot_roles():
    """
    If any completed donations exist that have never given roles  to
    discord tag, give roles for all of those donations. This task is 
    configured to run every 5 minutes.
    """
    donations_with_no_roles_given = CompletedDonation.objects.filter(
        gave_roles_count=0,
        completed=True
    )
    
    if donations_with_no_roles_given.count() > 0:
        for donation in donations_with_no_roles_given:
            if donation.bought_package.discord_roles.all().count() > 0:
                if not donation.discord_username:
                    continue
                
                donation.give_discord_roles()
                sleep(3)
                
@shared_task
def clear_donation_goal():
    """
    Set to run once a month, this will set the current donation goal
    progress back to 0
    """
    site_info:SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
    
    site_info.donation_goal_progress = 0
    site_info.save()
