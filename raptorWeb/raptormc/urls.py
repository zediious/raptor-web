from django.urls import URLPattern, path, re_path

from raptorWeb.raptormc import views
from raptorWeb.raptormc.routes import CURRENT_URLPATTERNS

app_name: str = "raptormc"

urlpatterns: list[URLPattern] = [

    path('raptormc/api/html/home', views.HomeServers.as_view(), name="home"),
    # Information
    path('raptormc/api/html/announcements', views.Announcements.as_view(), name="announcements"),
    path('raptormc/api/html/announcements/', views.Announcements.as_view(), name="announcements"),
    path('raptormc/api/html/rules', views.Rules.as_view(), name="rules"),
    path('raptormc/api/html/rules/', views.Rules.as_view(), name="rules"),
    path('raptormc/api/html/banneditems', views.BannedItems.as_view(), name="banneditems"),
    path('raptormc/api/html/banneditems/', views.BannedItems.as_view(), name="banneditems"),
    path('raptormc/api/html/voting', views.Voting.as_view(), name="voting"),
    path('raptormc/api/html/voting/', views.Voting.as_view(), name="voting"),
    path('raptormc/api/html/howtojoin', views.HowToJoin.as_view(), name="howtojoin"),
    path('raptormc/api/html/howtojoin/', views.HowToJoin.as_view(), name="howtojoin"),
    path('raptormc/api/html/applications', views.StaffApps.as_view(), name="applications"),
    path('raptormc/api/html/applications/', views.StaffApps.as_view(), name="applications"),
    path('raptormc/api/html/onboarding/<str:modpack_name>', views.Onboarding.as_view(), name="onboarding"),
    path('raptormc/api/html/onboarding/<str:modpack_name>/', views.Onboarding.as_view(), name="onboarding"),
    path('raptormc/api/html/donations', views.Donations.as_view(), name="donations"),
    path('raptormc/api/html/donations/', views.Donations.as_view(), name="donations"),
    path('raptormc/api/html/donations/checkout/<str:package>', views.DonationsCheckout.as_view(), name="donations/checkout"),
    path('raptormc/api/html/donations/checkout/<str:package>/', views.DonationsCheckout.as_view(), name="donations/checkout"),
    path('raptormc/api/html/donations/success', views.DonationsSuccess.as_view(), name="donations/success"),
    path('raptormc/api/html/donations/failure', views.DonationsFailure.as_view(), name="donations/failure"),
    path('raptormc/api/html/donations/failure/invalidusername', views.DonationsFailureInvalidUsername.as_view(), name="donations/failure/invalidusername"),
    path('raptormc/api/html/donations/failure/invalidprice', views.DonationsFailureInvalidPrice.as_view(), name="donations/failure/invalidprice"),
    path('raptormc/api/html/donations/previousdonation', views.DonationsAlreadyDonated.as_view(), name="donations/previousdonation"),
    # Created Pages
    path('raptormc/api/html/pages/<str:page_name>', views.PageView.as_view(), name="pages"),
    path('raptormc/api/html/pages/<str:page_name>/', views.PageView.as_view(), name="pages"),
    # Users
    path('raptormc/api/html/user', views.SiteMembers.as_view(), name='user'),
    path('raptormc/api/html/user/', views.SiteMembers.as_view(), name='user'),
    path('raptormc/api/html/user/<str:profile_name>', views.User_Page.as_view(), name="user_page"),
    path('raptormc/api/html/user/<str:profile_name>/', views.User_Page.as_view(), name="user_page"),
    path('raptormc/api/html/user/reset/<str:profile_name>/<str:user_reset_token>', views.User_Pass_Reset.as_view(), name="user_reset_pass"),
    # 404
    path('404', views.View_404.as_view(), name='404_view'),
    # API
    path('raptormc/api/action/session/headerbox/update', views.Update_Headerbox_State.as_view(), name='update_headerbox_state'),
    path('raptormc/api/crud/pages/delete/<int:pk>/', views.PageDelete.as_view(), name="page_delete"),
    path('raptormc/api/crud/toasts/delete/<int:pk>/', views.NotificationToastDelete.as_view(), name="toast_delete"),
    path('raptormc/api/crud/navbarlink/delete/<int:pk>/', views.NavbarLinkDelete.as_view(), name="navbarlink_delete"),
    path('raptormc/api/crud/navbardropdown/delete/<int:pk>/', views.NavbarDropdownDelete.as_view(), name="navbardropdown_delete"),
    path('raptormc/api/crud/navwidget/delete/<int:pk>/', views.NavWidgetDelete.as_view(), name="navwidget_delete"),
    path('raptormc/api/crud/navwidgetbar/delete/<int:pk>/', views.NavWidgetBarDelete.as_view(), name="navwidgetbar_delete"),
    # Base View
    re_path(r'\S*', views.BaseView.as_view(), name="base")

]

CURRENT_URLPATTERNS.append(urlpatterns)
