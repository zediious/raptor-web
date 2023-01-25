from django.urls import path

from raptorWeb.raptorbot import views

app_name = "raptorbot"

urlpatterns = [

    path('global_announcements_list/light', views.Global_Announcements.as_view(template_name='raptorbot/globalannouncement_list.html'), name="global_announcements_list"),
    path('global_announcements_list/dark', views.Global_Announcements.as_view(template_name='raptorbot/globalannouncement_list_dark.html'), name="global_announcements_list_dark"),
    path('server_announcements_list/', views.Server_Announcements.as_view(), name="server_announcements_list")

]