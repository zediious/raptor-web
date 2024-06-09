from django.urls import URLPattern, path, include

from raptorWeb.donations import views

app_name: str = "donations"

urlpatterns: list[URLPattern] = [
    path('packages', views.DonationPackages.as_view(), name="packages"),
    path('packages/', views.DonationPackages.as_view(), name="packages"),
    path('completeddonationspublic', views.CompletedDonationsPublic.as_view(template_name='donations/completeddonationpublic_list.html'), name="donations_public"),
    path('checkout/<str:package>', views.DonationCheckout.as_view(), name="checkout"),
    path('checkout/<str:package>/', views.DonationCheckout.as_view(), name="checkout"),
    path('checkout/<str:package>/redirect', views.DonationCheckoutRedirect.as_view(), name="stripe_redirect"),
    path('checkout/<str:package>/redirect/', views.DonationCheckoutRedirect.as_view(), name="stripe_redirect"),
    path('payment/cancel', views.DonationCancel.as_view(), name="cancel"),
    path('payment/cancel/', views.DonationCancel.as_view(), name="cancel"),
    path('payment/webhook', views.donation_payment_webhook, name="payment_webook"),
    path('payment/webhook/', views.donation_payment_webhook, name="payment_webook"),
    path('payment/paypal_webhook', include('paypal.standard.ipn.urls')),
    # Model Deletion
    path('donation/delete/', views.DonationDelete.as_view(), name="donation_delete"),
    path('crud/donationpackage/delete/<int:pk>', views.DonationPackageDelete.as_view(), name="donationpackage_delete"),
    path('crud/donationservercommand/delete/<int:pk>', views.DonationServerCommandDelete.as_view(), name="donationservercommand_delete"),
    path('crud/donationdiscordrole/delete/<int:pk>', views.DonationDiscordRoleDelete.as_view(), name="donationdiscordrole_delete"),
    # Admin
    path('donation/resend/', views.DonationBenefitResend.as_view(), name="resend"),
]