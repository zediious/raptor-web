from logging import getLogger
from uuid import uuid1

from django.http import HttpRequest
from django.shortcuts import redirect
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from raptorWeb.donations.models import DonationPackage, CompletedDonation
from raptorWeb.donations.tasks import send_server_commands, add_discord_bot_roles, send_donation_email
from raptorWeb.raptormc.models import SiteInformation

LOGGER = getLogger('donations.payments.paypal')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
DEBUG: str = getattr(settings, 'DEBUG')
PAYPAL_DEV_WEBHOOK_DOMAIN: str = getattr(settings, 'PAYPAL_DEV_WEBHOOK_DOMAIN')
PAYPAL_RECEIVER_EMAIL: str = getattr(settings, 'PAYPAL_RECEIVER_EMAIL')

def get_paypal_checkout_button(request: HttpRequest, bought_package: DonationPackage, minecraft_username: str, discord_username: str):
    site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
    invoice_id = f"raptor-{uuid1()}"
    
    try:
        CompletedDonation.objects.get(
            minecraft_username=minecraft_username,
            bought_package=bought_package,
            completed=False
        ).delete()

    except CompletedDonation.DoesNotExist:
        pass
    
    new_donation = CompletedDonation.objects.create(
        minecraft_username=minecraft_username,
        bought_package=bought_package,
        spent=bought_package.price,
        session_id=request.session.session_key,
        paypal_invoice=invoice_id,
        completed=False
    )
    
    if discord_username != '':
        new_donation.discord_username = discord_username
    
    if request.user.is_authenticated:
        new_donation.donating_user = request.user
        
    new_donation.save()
    
    form_data = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "amount": str(bought_package.price),
        'currency_code': site_info.donation_currency.upper(),
        "item_name": f"{bought_package.name} for {minecraft_username}",
        "invoice": invoice_id,
        "return": f'{WEB_PROTO}://{DOMAIN_NAME}/donations/success',
        "cancel_return": f'{WEB_PROTO}://{DOMAIN_NAME}/api/donations/payment/cancel',
    }
    
    if DEBUG:
        form_data.update({
            "notify_url": f'https://{PAYPAL_DEV_WEBHOOK_DOMAIN}/api/donations/payment/paypal_webhook',
        })
        
    else:
        form_data.update({
            "notify_url": f'{WEB_PROTO}://{DOMAIN_NAME}/api/donations/payment/paypal_webhook',
        })
    
    return PayPalPaymentsForm(initial=form_data)
    
