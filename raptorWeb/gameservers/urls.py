from django.urls import URLPattern, path

from raptorWeb.gameservers import views

app_name: str = "gameservers"

urlpatterns: list[URLPattern] = [

    # Server/Player ListViews
    path('html/total_count_poll/', views.Player_List.as_view(), name="totol_counts_poll"),
    path('html/total_count_poll_simple/', views.Player_List.as_view(template_name='gameservers/player_list_simple.html'), name="total_counts_poll_simple"),
    path('html/server_button_poll/', views.Server_Buttons.as_view(template_name='gameservers/server_list.html'), name="server_buttons_poll"),
    path('html/server_button_poll_loading/', views.Server_Buttons.as_view(template_name='gameservers/server_list_loading.html'), name="server_buttons_poll_loading"),
    path('html/server_modal_poll/', views.Server_List_Base.as_view(template_name='gameservers/server_list_modals.html'), name="server_modals_poll"),
    path('html/server_rules_poll/', views.Server_List_Base.as_view(template_name='gameservers/server_list_rules.html'), name="server_rules_poll"),
    path('html/server_banned_items_poll/', views.Server_List_Base.as_view(template_name='gameservers/server_list_banneditems.html'), name="server_banned_items_poll"),
    path('html/server_voting_poll/', views.Server_List_Base.as_view(template_name='gameservers/server_list_voting.html'), name="server_voting_poll"),
    path('html/server_announcements_poll/', views.Server_List_Base.as_view(template_name='gameservers/server_list_announcements.html'), name="server_announcements_poll"),
    # Forms
    path('html/forms/statistic_filter', views.Statistic_Filter_Form.as_view(), name="statistic_filter"),
    # Statistics
    path('html/statistics/player_counts', views.Player_Count_Statistics.as_view(), name="player_statistics_chart"),
    # Command API
    path('action/import_server_data/', views.Import_Servers.as_view(), name="action_import_server_data"),
    path('action/export_server_data/', views.Export_Servers.as_view(), name="action_export_server_data")

]