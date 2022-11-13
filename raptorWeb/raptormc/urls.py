from django.urls import path

from raptormc import views

SR = views.ShadowRaptor

app_name = "raptormc"

urlpatterns = [

    path('', SR.Info.HomeServers.as_view(), name="home"),
    path('home/', SR.Info.HomeServers.as_view(), name="home_alt"),
    path('announcements/', SR.Info.Announcements.as_view(), name="announcements"),
    path('rules/', SR.Info.Rules.as_view(), name="rules"),
    path('banneditems/', SR.Info.BannedItems.as_view(), name="banned_items"),
    path('voting/', SR.Info.Voting.as_view(), name="voting"),
    path('howtojoin/', SR.Info.HowToJoin.as_view(), name="joining"),
    path('applications/', SR.Info.StaffApps.as_view(), name="staff_apps"),
    path('applications/mod/', SR.Application.ModApp.as_view(), name="mod_app"),
    path('applications/admin/', SR.Application.AdminApp.as_view(), name="admin_app"),
    path('register/', SR.Application.RegisterUser.as_view(), name="register"),
    path('login/', SR.Application.UserLogin.as_view(), name="login"),
    path('logout/', SR.Application.user_logout, name="logout"),
    path('server_button_poll/', SR.Ajax_Views.Server_Buttons.as_view(), name="server_buttons_poll"),
    path('server_modal_poll/', SR.Ajax_Views.Server_Modals.as_view(), name="server_modals_poll"),
    path('total_count_poll/', SR.Ajax_Views.Total_Count.as_view(), name="totol_counts_poll")

]