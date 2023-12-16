from logging import getLogger

from django.conf import settings

import stripe

from raptorWeb.donations.models import DonationPackage

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
        success_url=f"{WEB_PROTO}://{DOMAIN_NAME}/api/donations/payment/success",
        cancel_url=f"{WEB_PROTO}://{DOMAIN_NAME}/api/donations/payment/cancel",
    )
