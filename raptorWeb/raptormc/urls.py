from django.urls import path

from raptorWeb.raptormc import views

SR = views.ShadowRaptor
app_name = "raptormc"

urlpatterns = [

    path('', SR.Info.HomeServers.as_view(), name="home"),
    path('home/', SR.Info.HomeServers.as_view(), name="home_alt"),
    # Information
    path('announcements/', SR.Info.Announcements.as_view(), name="announcements"),
    path('rules/', SR.Info.Rules.as_view(), name="rules"),
    path('banneditems/', SR.Info.BannedItems.as_view(), name="banned_items"),
    path('voting/', SR.Info.Voting.as_view(), name="voting"),
    path('howtojoin/', SR.Info.HowToJoin.as_view(), name="joining"),
    path('applications/', SR.Info.StaffApps.as_view(), name="staff_apps"),
    # Users
    path('user/', SR.User_Views.SiteMembers.as_view(), name='site_members'),
    path('user/<str:profile_name>', SR.User_Views.User_Page.as_view(), name="user_page"),
    path('user/reset/<str:profile_name>/<str:user_reset_token>', SR.User_Views.User_Pass_Reset.as_view(), name="user_reset_pass")

]
