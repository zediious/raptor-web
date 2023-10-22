from django.urls import URLPattern, path

from raptorWeb.raptormc import views
from raptorWeb.raptormc.exchange import current_urlpatterns

app_name: str = "raptormc"

urlpatterns: list[URLPattern] = [

    path('', views.HomeServers.as_view(), name="home"),
    # Information
    path('announcements', views.Announcements.as_view(), name="announcements"),
    path('announcements/', views.Announcements.as_view(), name="announcements_slash"),
    path('rules', views.Rules.as_view(), name="rules"),
    path('rules/', views.Rules.as_view(), name="rules"),
    path('banneditems', views.BannedItems.as_view(), name="banned_items"),
    path('banneditems/', views.BannedItems.as_view(), name="banned_items_slash"),
    path('voting', views.Voting.as_view(), name="voting"),
    path('voting/', views.Voting.as_view(), name="voting_slash"),
    path('howtojoin', views.HowToJoin.as_view(), name="joining"),
    path('howtojoin/', views.HowToJoin.as_view(), name="joining_slash"),
    path('applications', views.StaffApps.as_view(), name="staff_apps"),
    path('applications/', views.StaffApps.as_view(), name="staff_apps_slash"),
    # Created Pages
    path('pages/<str:page_name>', views.PageView.as_view(), name="pages"),
    # Users
    path('user/', views.SiteMembers.as_view(), name='site_members'),
    path('user/<str:profile_name>', views.User_Page.as_view(), name="user_page"),
    path('user/reset/<str:profile_name>/<str:user_reset_token>', views.User_Pass_Reset.as_view(), name="user_reset_pass"),
    # Admin Panel
    path('panel/', views.Admin_Panel.as_view(), name='admin_panel_base'),
    # 404
    path('404', views.View_404.as_view(), name='404_view'),
    # API
    path('api/session/headerbox/update', views.Update_Headerbox_State.as_view(), name='update_headerbox_state')

]

current_urlpatterns.append(urlpatterns)
