from django.urls import path

from raptorWeb.raptormc import views

app_name = "raptormc"

urlpatterns = [

    path('', views.HomeServers.as_view(), name="home"),
    path('home/', views.HomeServers.as_view(), name="home_alt"),
    # Information
    path('announcements/', views.Announcements.as_view(), name="announcements"),
    path('rules/', views.Rules.as_view(), name="rules"),
    path('banneditems/', views.BannedItems.as_view(), name="banned_items"),
    path('voting/', views.Voting.as_view(), name="voting"),
    path('howtojoin/', views.HowToJoin.as_view(), name="joining"),
    path('applications/', views.StaffApps.as_view(), name="staff_apps"),
    # Users
    path('user/', views.SiteMembers.as_view(), name='site_members'),
    path('user/<str:profile_name>', views.User_Page.as_view(), name="user_page"),
    path('user/reset/<str:profile_name>/<str:user_reset_token>', views.User_Pass_Reset.as_view(), name="user_reset_pass"),
    # Admin Panel
    path('panel/', views.Admin_Panel.as_view(), name='admin_panel_base')

]
