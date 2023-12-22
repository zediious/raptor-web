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
    path('api/html/panel/serveractions', views.ServerActionsPanel.as_view(), name="serveractions"),
    path('api/html/panel/serveractions/', views.ServerActionsPanel.as_view(), name="serveractions"),
    path('api/html/panel/reporting', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/reporting/', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/donations/', views.DonationsPanel.as_view(), name="donations"),
    path('api/html/panel/settings', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/files/update', views.SettingsPanelFilePost.as_view(), name="settings_files_update"),
    path('api/html/panel/settings/defaultpagese/update', views.SettingsPanelDefaultPagesPost.as_view(), name="settings_default_pages"),
    # Admin Panel Base View
    re_path(r'\S*', views.BaseView.as_view(), name='admin_panel_base'),

]

CURRENT_URLPATTERNS.append(urlpatterns)
