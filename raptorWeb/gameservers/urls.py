from django.urls import path

from gameservers import views

app_name = "gameservers"

urlpatterns = [

    path('server_button_poll/', views.Server_Buttons.as_view(), name="server_buttons_poll"),
    path('server_button_poll_loading/', views.Server_Buttons_Loading.as_view(), name="server_buttons_poll_loading"),
    path('server_modal_poll/', views.Server_Modals.as_view(), name="server_modals_poll"),
    path('total_count_poll/', views.Total_Count.as_view(), name="totol_counts_poll"),
    path('server_rules_poll/', views.Server_Rules.as_view(), name="server_rules_poll"),
    path('server_banned_items_poll/', views.Server_Banned_Items.as_view(), name="server_banned_items_poll"),
    path('server_voting_poll/', views.Server_Voting.as_view(), name="server_voting_poll"),
    path('server_announcements_poll/', views.Server_Announcements.as_view(), name="server_announcements_poll")

]