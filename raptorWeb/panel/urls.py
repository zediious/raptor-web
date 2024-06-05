from django.urls import URLPattern, path, re_path

from raptorWeb.panel import views
from raptorWeb.panel.routes import CURRENT_URLPATTERNS

app_name: str = "panel"

urlpatterns: list[URLPattern] = [

    # Panel Tab API
    path('api/html/panel/home', views.HomePanel.as_view(), name="home"),
    path('api/html/panel/home/', views.HomePanel.as_view(), name="home"),
    path('api/html/panel/discordbot', views.DiscordBotPanel.as_view(), name="discordbot"),
    path('api/html/panel/discordbot/', views.DiscordBotPanel.as_view(), name="discordbot"),
    path('api/html/panel/server/importexport', views.ServerActionsPanel.as_view(), name="server/importexport"),
    path('api/html/panel/server/importexport/', views.ServerActionsPanel.as_view(), name="server/importexport"),
    path('api/html/panel/server/list/', views.PanelServerList.as_view(template_name='panel/crud/server_list.html'), name="server/list"),
    path('api/html/panel/server/archivedlist', views.PanelServerList.as_view(template_name='panel/crud/server_list_archived.html'), name="server/archivedlist"),
    path('api/html/panel/server/update/<int:pk>', views.PanelServerUpdate.as_view(template_name='panel/crud/server_update.html'), name="server/update_IR"),
    path('api/html/panel/server/create/', views.PanelServerCreate.as_view(template_name='panel/crud/server_create.html'), name="server/create"),
    path('api/html/panel/player/list/', views.PanelPlayerList.as_view(template_name='panel/crud/player_list.html'), name="player/list"),
    path('api/html/panel/content/informativetext/list', views.PanelInformativeTextList.as_view(template_name='panel/crud/informativetext_list.html'), name="content/informativetext/list"),
    path('api/html/panel/content/informativetext/update/<int:pk>', views.PanelInformativeTextUpdate.as_view(template_name='panel/crud/informativetext_update.html'), name="content/informativetext/update_IR"),
    path('api/html/panel/reporting', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/reporting/', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/donations/', views.DonationsPanel.as_view(), name="donations"),
    path('api/html/panel/settings', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/files/update', views.SettingsPanelFilePost.as_view(), name="settings_files_update"),
    path('api/html/panel/settings/defaultpages/update', views.SettingsPanelDefaultPagesPost.as_view(), name="settings_default_pages"),
    # Admin Panel Base View
    re_path(r'\S*', views.BaseView.as_view(), name='admin_panel_base'),

]

CURRENT_URLPATTERNS.append(urlpatterns)
