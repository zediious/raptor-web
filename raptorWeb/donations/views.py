from logging import getLogger
from os.path import join
from typing import Any

from django.views.generic import ListView, TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rcon.source import Client
from stripe import Webhook
from stripe.error import SignatureVerificationError

from raptorWeb.donations.models import DonationPackage, CompletedDonation
from raptorWeb.donations.forms import SubmittedDonationForm
from raptorWeb.donations.payments import get_checkout_url

DONATIONS_TEMPLATE_DIR: str = getattr(settings, 'DONATIONS_TEMPLATE_DIR')
STRIPE_WEBHOOK_SECRET:str = getattr(settings, 'STRIPE_WEBHOOK_SECRET')

LOGGER = getLogger('donations.views')
    
    
class DonationPackages(ListView):
    """
    ListView for all created DonationPackages
    """
    paginate_by: int = 9
    model: DonationPackage = DonationPackage

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
        
class DonationCheckout(TemplateView):
    """
    Pre-checkout page before redirect to payment
    """
    template_name: str = join(DONATIONS_TEMPLATE_DIR, 'checkout.html')

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['buying_package'] = str(self.kwargs['package'])
        context['minecraft_username_form'] = SubmittedDonationForm()
        return context
        
        
class DonationCheckoutRedirect(View):
    """
    Handle redirect to Stripe payment gateway
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """
        Utilized when a donator is logged in
        """
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        
        try:
            bought_package = DonationPackage.objects.get(name=str(self.kwargs['package']))
            
        except DonationPackage.DoesNotExist:
            return HttpResponseRedirect('/')
        
        return redirect(
            get_checkout_url(
                request,
                bought_package,
                request.user.user_profile_info.minecraft_username
            )
        )
        
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """
        Utilized when a donator is not logged in
        """
        if not request.POST.get('minecraft_username'):
            return HttpResponseRedirect('/')
        
        try:
            bought_package = DonationPackage.objects.get(name=str(self.kwargs['package']))
            
        except DonationPackage.DoesNotExist:
            return HttpResponseRedirect('/')
        
        return redirect(
            get_checkout_url(
                request,
                bought_package,
                request.POST.get('minecraft_username'),
            )
        )
        
        
class DonationCancel(View):
    """
    Delete created donation if it is cancelled
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        try:
            CompletedDonation.objects.filter(
                session_id=request.session.session_key,
                completed=False
            ).delete()
            
            return HttpResponseRedirect('/donations/failure')
        
        except CompletedDonation.DoesNotExist:
            return HttpResponseRedirect('/donations/failure')
        

@csrf_exempt
def donation_payment_webhook(request: HttpRequest):
    """
    Webhook to listen for payment events from Stripe
    """
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET
            )
            
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        
        except SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)
        
        except:
            # Uncaught error
            return HttpResponse(status=400)

        # Passed signature verification
        if event['type'] == 'checkout.session.completed':
            completed_donation = CompletedDonation.objects.get(
                checkout_id=event['data']['object']['id'],
                completed=False
            )
            completed_donation.completed = True
            completed_donation.save()
            
        elif event['type'] == 'checkout.session.expired':
            completed_donation = CompletedDonation.objects.get(
                checkout_id=event['data']['object']['id'],
                completed=False
            )
            completed_donation.delete()
        
        return HttpResponse(status=200)
        