from django.urls import URLPattern, path

from raptorWeb.raptormc import views

app_name: str = "raptormc"

urlpatterns: list[URLPattern] = [

    path('', views.HomeServers.as_view(), name="home"),
    path('home/', views.HomeServers.as_view(), name="home_alt"),
    # Information
    path('announcements/', views.Announcements.as_view(), name="announcements"),
    path('rules/', views.Rules.as_view(), name="rules"),
    path('banneditems/', views.BannedItems.as_view(), name="banned_items"),
    path('voting/', views.Voting.as_view(), name="voting"),
    path('howtojoin/', views.HowToJoin.as_view(), name="joining"),
    path('applications/', views.StaffApps.as_view(), name="staff_apps"),
    # Created Pages
    path('pages/<str:page_name>/', views.PageView.as_view(), name="pages"),
    # Users
    path('user/', views.SiteMembers.as_view(), name='site_members'),
    path('user/<str:profile_name>', views.User_Page.as_view(), name="user_page"),
    path('user/reset/<str:profile_name>/<str:user_reset_token>', views.User_Pass_Reset.as_view(), name="user_reset_pass"),
    # Admin Panel
    path('panel/', views.Admin_Panel.as_view(), name='admin_panel_base'),
    # 404
    path('404', views.View_404.as_view(), name='404_view')

]
