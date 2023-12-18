from django.urls import URLPattern, path

from raptorWeb.donations import views

app_name: str = "donations"

urlpatterns: list[URLPattern] = [
    path('packages', views.DonationPackages.as_view(), name="packages"),
    path('packages/', views.DonationPackages.as_view(), name="packages"),
    path('completeddonations', views.CompletedDonations.as_view(), name="donations"),
    path('checkout/<str:package>', views.DonationCheckout.as_view(), name="checkout"),
    path('checkout/<str:package>/', views.DonationCheckout.as_view(), name="checkout"),
    path('checkout/<str:package>/redirect', views.DonationCheckoutRedirect.as_view(), name="stripe_redirect"),
    path('checkout/<str:package>/redirect/', views.DonationCheckoutRedirect.as_view(), name="stripe_redirect"),
    path('payment/cancel', views.DonationCancel.as_view(), name="cancel"),
    path('payment/cancel/', views.DonationCancel.as_view(), name="cancel"),
    path('payment/webhook', views.donation_payment_webhook, name="payment_webook"),
    path('payment/webhook/', views.donation_payment_webhook, name="payment_webook"),
    # Admin
    path('donation/resend/', views.DonationBenefitResend.as_view(), name="resend"),
]