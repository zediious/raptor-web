from django.urls import URLPattern, path

from raptorWeb.raptorbot import views

app_name: str = "raptorbot"

urlpatterns: list[URLPattern] = [

    # ListViews
    path('html/global_announcements_list/light/<int:amount>/', views.Global_Announcements.as_view(template_name='raptorbot/globalannouncement_list.html'), name="global_announcements_list"),
    path('html/global_announcements_list/dark/', views.Global_Announcements.as_view(template_name='raptorbot/globalannouncement_list_dark.html'), name="global_announcements_list_dark"),
    path('html/server_announcements_list/<int:server_pk>/', views.Server_Announcements.as_view(), name="server_announcements_list"),
    # Bot Start and Stop
    path('action/botstatus/get/', views.Get_Bot_Status.as_view(), name="botstatus_get"),
    path('action/botstatus/start/', views.Start_Bot.as_view(), name="botstatus_start_bot"),
    path('action/botstatus/stop/', views.Stop_Bot.as_view(), name="botstatus_stop_bot"),
    # Command API
    path('action/command/refresh_global_announcements/', views.Update_Global_Announcement.as_view(), name="command_update_global_announcements"),
    path('action/command/refresh_all_server_announcements/', views.Update_Server_Announcement.as_view(), name="command_update_all_server_announcements"),
    path('action/command/update_members/', views.Update_Members.as_view(), name="command_update_members")

]