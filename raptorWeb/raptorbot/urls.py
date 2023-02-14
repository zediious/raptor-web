from django.urls import path

from raptorWeb.raptorbot import views

app_name = "raptorbot"

urlpatterns = [

    path('html/global_announcements_list/light/<int:amount>/', views.Global_Announcements.as_view(template_name='raptorbot/globalannouncement_list.html'), name="global_announcements_list"),
    path('html/global_announcements_list/dark/', views.Global_Announcements.as_view(template_name='raptorbot/globalannouncement_list_dark.html'), name="global_announcements_list_dark"),
    path('html/server_announcements_list/<int:server_pk>/', views.Server_Announcements.as_view(), name="server_announcements_list")

]