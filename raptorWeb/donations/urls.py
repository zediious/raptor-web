from django.urls import URLPattern, path

from raptorWeb.donations import views

app_name: str = "donations"

urlpatterns: list[URLPattern] = [
    path('packages', views.DonationPackages.as_view(), name="packages"),
    path('packages/', views.DonationPackages.as_view(), name="packages"),
    path('checkout', views.DonationCheckout.as_view(), name="checkout"),
    path('checkout/', views.DonationCheckout.as_view(), name="checkout"),
    path('checkout/redirect', views.DonationCheckoutRedirect.as_view(), name="stripe_redirect"),
    path('checkout/redirect/', views.DonationCheckoutRedirect.as_view(), name="stripe_redirect"),
    path('payment/success', views.DonationSuccess.as_view(), name="success"),
    path('payment/success/', views.DonationSuccess.as_view(), name="success"),
    path('payment/cancel', views.DonationCancel.as_view(), name="cancel"),
    path('payment/cancel/', views.DonationCancel.as_view(), name="cancel"),
    path('payment/webhook', views.donation_payment_webhook, name="payment_webook"),
    path('payment/webhook/', views.donation_payment_webhook, name="payment_webook"),
]