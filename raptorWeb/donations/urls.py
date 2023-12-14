from django.urls import URLPattern, path

from raptorWeb.donations import views

app_name: str = "donations"

urlpatterns: list[URLPattern] = [
    path('packages', views.DonationPackages.as_view(), name="packages"),
    path('packages/', views.DonationPackages.as_view(), name="packages"),
]