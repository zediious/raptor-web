from logging import getLogger

from django.conf import settings

import stripe

from raptorWeb.donations.models import DonationPackage, CompletedDonation

LOGGER = getLogger('donations.payments')
DOMAIN_NAME: str = getattr(settings, 'DOMAIN_NAME')
WEB_PROTO: str = getattr(settings, 'WEB_PROTO')
STRIPE_PUBLISHABLE_KEY: str = getattr(settings, 'STRIPE_PUBLISHABLE_KEY')
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY')

def create_checkout_session(package: DonationPackage, mninecraft_username: str):
    """
    Create a Stripe Checkout Session, using the Donation Package
    and Minecraft Username passed as arguments, and return it.
    """
    return stripe.checkout.Session.create(
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': f'{package.name} for {mninecraft_username}',
                    },
                    'unit_amount': package.price * 100,
                },
                'quantity': 1,
        }],
        mode="payment",
        success_url=f"{WEB_PROTO}://{DOMAIN_NAME}/donations/success",
        cancel_url=f"{WEB_PROTO}://{DOMAIN_NAME}/api/donations/payment/cancel",
    )
    
def retrieve_checkout_session(checkout_id: str):
    """
    Retrieve a Stripe Checkout session given the session's ID
    """
    return stripe.checkout.Session.retrieve(
        id=checkout_id
    )
    
def get_checkout_url(request,  bought_package: DonationPackage, minecraft_username: str, discord_username: str):
    """
    Return a checkout URL for the given request
    """
    checkout_url: str = ''
        
    try:
        incomplete_donation = CompletedDonation.objects.get(
            minecraft_username=minecraft_username,
            bought_package=bought_package,
            completed=False
        )
        
        checkout_url = retrieve_checkout_session(incomplete_donation.checkout_id).url
        
    except CompletedDonation.DoesNotExist:
        checkout_session = create_checkout_session(
            bought_package,
            minecraft_username
        )
        
        checkout_url = checkout_session.url
    
        new_donation = CompletedDonation.objects.create(
            minecraft_username=minecraft_username,
            bought_package=bought_package,
            session_id=request.session.session_key,
            checkout_id=checkout_session.id,
            completed=False
        )
        
        if discord_username != '':
            new_donation.discord_username = discord_username
        
        if request.user.is_authenticated:
            new_donation.donating_user = request.user
            
        new_donation.save()
        
    return checkout_url