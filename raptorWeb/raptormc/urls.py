from django.urls import URLPattern, path, re_path
from django import apps

from raptorWeb.raptormc import views
from raptorWeb.raptormc.routes import CURRENT_URLPATTERNS, ALL_ROUTED_MODELS

app_name: str = "raptormc"

urlpatterns: list[URLPattern] = [

    path('raptormc/api/html/home', views.HomeServers.as_view(), name="home"),
    # Information
    path('raptormc/api/html/announcements', views.Announcements.as_view(), name="announcements"),
    path('raptormc/api/html/announcements/', views.Announcements.as_view(), name="announcements_IR"),
    path('raptormc/api/html/rules', views.Rules.as_view(), name="rules"),
    path('raptormc/api/html/rules/', views.Rules.as_view(), name="rules_IR"),
    path('raptormc/api/html/banneditems', views.BannedItems.as_view(), name="banneditems"),
    path('raptormc/api/html/banneditems/', views.BannedItems.as_view(), name="banneditems_IR"),
    path('raptormc/api/html/voting', views.Voting.as_view(), name="voting"),
    path('raptormc/api/html/voting/', views.Voting.as_view(), name="voting_IR"),
    path('raptormc/api/html/howtojoin', views.HowToJoin.as_view(), name="howtojoin"),
    path('raptormc/api/html/howtojoin/', views.HowToJoin.as_view(), name="howtojoin_IR"),
    path('raptormc/api/html/applications', views.StaffApps.as_view(), name="applications"),
    path('raptormc/api/html/applications/', views.StaffApps.as_view(), name="applications_IR"),
    path('raptormc/api/html/onboarding/<str:modpack_name>', views.Onboarding.as_view(), name="onboarding_IR"),
    path('raptormc/api/html/onboarding/<str:modpack_name>/', views.Onboarding.as_view(), name="onboarding_IR"),
    path('raptormc/api/html/donations', views.Donations.as_view(), name="donations"),
    path('raptormc/api/html/donations/', views.Donations.as_view(), name="donations_IR"),
    path('raptormc/api/html/donations/checkout/<str:package>', views.DonationsCheckout.as_view(), name="donations/checkout_IR"),
    path('raptormc/api/html/donations/checkout/<str:package>/', views.DonationsCheckout.as_view(), name="donations/checkout_IR"),
    path('raptormc/api/html/donations/success', views.DonationsSuccess.as_view(), name="donations/success"),
    path('raptormc/api/html/donations/failure', views.DonationsFailure.as_view(), name="donations/failure"),
    path('raptormc/api/html/donations/failure/invalidusername', views.DonationsFailureInvalidUsername.as_view(), name="donations/failure/invalidusername"),
    path('raptormc/api/html/donations/failure/invalidprice', views.DonationsFailureInvalidPrice.as_view(), name="donations/failure/invalidprice"),
    path('raptormc/api/html/donations/previousdonation', views.DonationsAlreadyDonated.as_view(), name="donations/previousdonation"),
    # Created Pages
    path('raptormc/api/html/pages/<str:page_name>', views.PageView.as_view(), name="pages_IR"),
    path('raptormc/api/html/pages/<str:page_name>/', views.PageView.as_view(), name="pages_IR"),
    # Users
    path('raptormc/api/html/user', views.SiteMembers.as_view(), name='user'),
    path('raptormc/api/html/user/', views.SiteMembers.as_view(), name='user_IR'),
    path('raptormc/api/html/user/<str:profile_name>', views.User_Page.as_view(), name="user_page_IR"),
    path('raptormc/api/html/user/<str:profile_name>/', views.User_Page.as_view(), name="user_page_IR"),
    path('raptormc/api/html/user/reset/<str:profile_name>/<str:user_reset_token>', views.User_Pass_Reset.as_view(), name="user_reset_pass_IR"),
    # 404
    path('404', views.View_404.as_view(), name='404_view_IR'),
    # API
    path('raptormc/api/action/session/headerbox/update', views.Update_Headerbox_State.as_view(), name='update_headerbox_state'),
    # Base View
    re_path(r'\S*', views.BaseView.as_view(), name="base_IR")

]

for model in apps.registry.apps.get_models():
    try:
        if model.route_name:
            ALL_ROUTED_MODELS.append(model)
            
    except AttributeError:
        continue

CURRENT_URLPATTERNS.append(urlpatterns)
