from django.urls import path

from raptorWeb.gameservers import views

app_name = "gameservers"

urlpatterns = [

    path('server_button_poll/', views.Server_Buttons.as_view(), name="server_buttons_poll"),
    path('server_button_poll_loading/', views.Server_Buttons_Loading.as_view(template_name='gameservers/server_list_loading.html'), name="server_buttons_poll_loading"),
    path('server_modal_poll/', views.Server_Modals.as_view(template_name='gameservers/serverModals.html'), name="server_modals_poll"),
    path('total_count_poll/', views.Player_List.as_view(), name="totol_counts_poll"),
    path('server_rules_poll/', views.Server_Rules.as_view(template_name='gameservers/server_list_rules.html'), name="server_rules_poll"),
    path('server_banned_items_poll/', views.Server_Banned_Items.as_view(template_name='gameservers/server_list_banneditems.html'), name="server_banned_items_poll"),
    path('server_voting_poll/', views.Server_Voting.as_view(template_name='gameservers/server_list_voting.html'), name="server_voting_poll"),
    path('server_announcements_poll/', views.Server_Announcements_Base.as_view(template_name='gameservers/server_list_announcements.html'), name="server_announcements_poll")

]