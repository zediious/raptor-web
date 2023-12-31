from logging import getLogger
from os.path import join
from typing import Any

from django.views.generic import ListView, TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.db.models.query import QuerySet
from django.contrib import messages
from django.conf import settings

from stripe import Webhook
from stripe.error import SignatureVerificationError

from raptorWeb.raptormc.models import DefaultPages, SiteInformation
from raptorWeb.donations.models import DonationPackage, CompletedDonation
from raptorWeb.donations.forms import SubmittedDonationForm, DonationDiscordUsernameForm, DonationPriceForm, DonationGatewayForm
from raptorWeb.donations.tasks import send_server_commands, add_discord_bot_roles, send_donation_email
from raptorWeb.donations.mojang import verify_minecraft_username
from raptorWeb.donations.payments.stripe import get_checkout_url
from raptorWeb.donations.payments.paypal import get_paypal_checkout_button

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
        
        if not request.user.has_perm('raptormc.donations'):
            return HttpResponseRedirect('/404')
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_queryset(self) -> QuerySet[Any]:
        return CompletedDonation.objects.all().order_by('-donation_datetime')
    
    
class CompletedDonationsPublic(ListView):
    """
    ListView for the last 5 completed donations
    This is public facing
    """
    model: CompletedDonation = CompletedDonation

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_queryset(self) -> QuerySet[Any]:
        return CompletedDonation.objects.all().order_by('-donation_datetime')[:5]
    
    
class DonationPackages(ListView):
    """
    ListView for all created DonationPackages
    """
    paginate_by: int = 9
    model: DonationPackage = DonationPackage
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().order_by('priority')

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
        
        percent_progress = 100 * float(site_info.donation_goal_progress)/float(site_info.donation_goal)
        
        context.update({
            'donation_goal': site_info.donation_goal,
            'donation_goal_progress': site_info.donation_goal_progress,
            'donation_goal_percent': percent_progress,
            'show_donation_goal': site_info.show_donation_goal,
            'show_recent_donators': site_info.show_recent_donators,
            'donation_currency': site_info.donation_currency
        })
        
        return context

     
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
        
        site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
        bought_package = DonationPackage.objects.get(name=str(self.kwargs['package']))
        
        context['buying_package'] = bought_package
        context['base_user_url'] = BASE_USER_URL
        context['donation_price_form'] = DonationPriceForm({'chosen_price': bought_package.price})
        context['discord_username_form'] = DonationDiscordUsernameForm()
        context['donation_details_form'] = SubmittedDonationForm()
        
        if site_info.paypal_enabled and site_info.stripe_enabled:
            context['donation_gateway_form'] = DonationGatewayForm()
            context['single_gateway'] = False
            
        else:
            context['single_gateway'] = True
            
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
                return HttpResponseRedirect('/donations/failure')
            
        if verify_minecraft_username(minecraft_username) == None:
            return HttpResponseRedirect('/donations/failure/invalidusername')
        
        try:
            bought_package = DonationPackage.objects.get(name=str(self.kwargs['package']))
            
        except DonationPackage.DoesNotExist:
            return HttpResponseRedirect('/')
        
        site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
        
        if site_info.paypal_enabled and site_info.stripe_enabled:
            payment_gateway_choice = request.POST.get('payment_gateway')
            
        elif site_info.paypal_enabled == False and site_info.stripe_enabled:
            payment_gateway_choice = 'stripe'
            
        elif site_info.paypal_enabled and site_info.stripe_enabled == False:
            payment_gateway_choice = 'paypal'
        
        if bought_package.variable_price:
            chosen_price = request.POST.get('chosen_price')
            if int(chosen_price) < bought_package.price:
                return HttpResponseRedirect('/donations/failure/invalidprice')
            
            bought_package.price = int(chosen_price)
        
        if not bought_package.allow_repeat:
        
            if CompletedDonation.objects.filter(
                minecraft_username=minecraft_username,
                bought_package=bought_package,
                completed=True
                ).count() > 0:
                
                return HttpResponseRedirect('/donations/previousdonation')
            
        if payment_gateway_choice == 'stripe':
            if site_info.stripe_enabled:
                return redirect(
                    get_checkout_url(
                        request,
                        bought_package,
                        minecraft_username,
                        discord_username
                    )
                )
                
            else:
                return HttpResponseRedirect('/donations/failure')
            
        if payment_gateway_choice == 'paypal': 
            if site_info.paypal_enabled:
                paypal_button = get_paypal_checkout_button(
                    request,
                    bought_package,
                    minecraft_username,
                    discord_username
                )
                
                return render(
                    request,
                    join(DONATIONS_TEMPLATE_DIR, 'paypal_checkout_redirect.html'),
                    context={'form': paypal_button}
                )
                
            else:
                return HttpResponseRedirect('/donations/failure')
        
        return HttpResponseRedirect('/donations/failure')
        
        
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
        
        
class DonationDelete(View):
    """
    Delete a created donation
    """
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        if not request.user.is_staff:
            return HttpResponseRedirect('/404')
        
        if not request.user.has_perm('raptormc.donations'):
            return HttpResponseRedirect('/404')
        
        try:
            CompletedDonation.objects.get(
                pk=request.GET.get('donation_id')
            ).delete()
            
            messages.success(request, 'Donation has been deleted.')
            return HttpResponse(status=200)
        
        except CompletedDonation.DoesNotExist:
            messages.error(request, 'There was an error processing this package deletion')
            return HttpResponse(status=400)
        
        
class DonationBenefitResend(View):
    """
    Re-send benefits for a given completed donation
    """
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not DefaultPages.objects.get_or_create(pk=1)[0].donations:
            return HttpResponseRedirect('/404')
        
        if not request.user.is_staff:
            return HttpResponseRedirect('/404')
        
        if not request.user.has_perm('raptormc.donations'):
            return HttpResponseRedirect('/404')
        
        do_commands = request.GET.get('do_commands')
        do_roles = request.GET.get('do_roles')
        completed_donation = CompletedDonation.objects.get(
            id=request.GET.get('id')
        )
        
        if do_commands == 'true':
            if completed_donation.bought_package.commands.all().count() > 0:
                completed_donation.send_server_commands()
                messages.success(request, f'Re-sent server commands for {completed_donation.minecraft_username}')
            
            else:
                messages.error(request, f'Cannot re-send commands for this donation, the package has no commands to send!')
            
        if do_roles == 'true':
            if completed_donation.bought_package.discord_roles.all().count() > 0 and completed_donation.discord_username != None:
                completed_donation.give_discord_roles()
                messages.success(request, f'Re-gave Discord Roles for {completed_donation.discord_username}')
                
            else:
                messages.error(request, f'Cannot re-give Discord Roles for this donation, the package has no roles to give '
                                        'or the donation was not made with a Discord Username')
                
        return HttpResponse(status=200)
        

@csrf_exempt
def donation_payment_webhook(request: HttpRequest):
    """
    Webhook to listen for payment events from Stripe
    """
    if STRIPE_WEBHOOK_SECRET == '':
        return HttpResponseRedirect('/404')
    
    site_info: SiteInformation = SiteInformation.objects.get_or_create(pk=1)[0]
    
    if site_info.stripe_enabled == False:
        return HttpResponseRedirect('/404')
    
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
                    args=(completed_donation.pk,),
                    countdown=10
                )
                
            if completed_donation.bought_package.discord_roles.all().count() > 0:
                add_discord_bot_roles.apply_async(
                    args=(completed_donation.pk,),
                    countdown=5
                )
                
                LOGGER.info((f'{completed_donation.minecraft_username} has donated '
                f'for the {completed_donation.bought_package} package'))
                
            completed_donation.save()
            
            if site_info.send_donation_email:
                send_donation_email.apply_async(
                    args=(completed_donation.pk,),
                    countdown=5
                )
                
            site_info.donation_goal_progress += completed_donation.spent
            site_info.save()
            
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
        