from logging import getLogger
from os.path import join
from typing import Any

from django.views.generic import ListView, TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from stripe import Webhook
from stripe.error import SignatureVerificationError

from raptorWeb.raptormc.models import DefaultPages
from raptorWeb.donations.models import DonationPackage, CompletedDonation
from raptorWeb.donations.forms import SubmittedDonationForm, DonationDiscordUsernameForm, DonationPriceForm
from raptorWeb.donations.tasks import send_server_commands, add_discord_bot_roles
from raptorWeb.donations.payments import get_checkout_url

DONATIONS_TEMPLATE_DIR: str = getattr(settings, 'DONATIONS_TEMPLATE_DIR')
BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')
STRIPE_WEBHOOK_SECRET:str = getattr(settings, 'STRIPE_WEBHOOK_SECRET')

LOGGER = getLogger('donations.views')


class CompletedDonations(ListView):
    """
    ListView for all completed donations
    """
    paginate_by: int = 9
    model: CompletedDonation = CompletedDonation

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        if not request.user.has_perm('raptormc.server_actions'):
            return HttpResponseRedirect('/404')
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_queryset(self) -> QuerySet[Any]:
        return CompletedDonation.objects.all().order_by('-donation_datetime')
    
    
class DonationPackages(ListView):
    """
    ListView for all created DonationPackages
    """
    paginate_by: int = 9
    model: DonationPackage = DonationPackage

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
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
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        bought_package = DonationPackage.objects.get(name=str(self.kwargs['package']))
        context['buying_package'] = bought_package
        context['base_user_url'] = BASE_USER_URL
        context['donation_price_form'] = DonationPriceForm({'chosen_price': bought_package.price})
        context['discord_username_form'] = DonationDiscordUsernameForm()
        context['donation_details_form'] = SubmittedDonationForm()
        return context
        
        
class DonationCheckoutRedirect(View):
    """
    Handle redirect to Stripe payment gateway
    """        
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        try:
            minecraft_username: str = request.POST.get('minecraft_username')
            discord_username: str = request.POST.get('discord_username')
            
        except:
            minecraft_username: str = ''
            discord_username: str = ''
            
        if not request.POST.get('minecraft_username'):
            try:
                minecraft_username: str = request.user.user_profile_info.minecraft_username
                discord_username: str = request.user.discord_user_info.tag
                
            except AttributeError:
                pass
                
            if not request.user.is_authenticated:
                return HttpResponseRedirect('/')
        
        try:
            bought_package = DonationPackage.objects.get(name=str(self.kwargs['package']))
            
        except DonationPackage.DoesNotExist:
            return HttpResponseRedirect('/')
        
        if bought_package.variable_price:
            chosen_price = request.POST.get('chosen_price')
            bought_package.price = int(chosen_price)
        
        if not bought_package.allow_repeat:
        
            if CompletedDonation.objects.filter(
                minecraft_username=minecraft_username,
                bought_package=bought_package,
                completed=True
                ).count() > 0:
                
                return HttpResponseRedirect('/donations/previousdonation')
        
        return redirect(
            get_checkout_url(
                request,
                bought_package,
                minecraft_username,
                discord_username
            )
        )
        
        
class DonationCancel(View):
    """
    Delete created donation if it is cancelled
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
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
    if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
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
            if completed_donation.bought_package.servers.all().count() > 0:
                send_server_commands.apply_async(
                    args=(completed_donation.checkout_id,),
                    countdown=10
                )
                add_discord_bot_roles.apply_async(
                    args=(completed_donation.checkout_id,),
                    countdown=5
                )
                
                LOGGER.info((f'{completed_donation.minecraft_username} has donated '
                f'for the {completed_donation.bought_package} package'))
                
            completed_donation.save()
            
        elif event['type'] == 'checkout.session.expired':
            try: 
                completed_donation = CompletedDonation.objects.get(
                    checkout_id=event['data']['object']['id'],
                    completed=False
                )
                completed_donation.delete()
            
            except CompletedDonation.DoesNotExist:
                LOGGER.info(f"Did not find {event['data']['object']['id']}. The donation was already deleted.")
                pass
        
        return HttpResponse(status=200)
        