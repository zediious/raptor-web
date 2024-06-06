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
    path('api/html/panel/content/page/list', views.PanelPageList.as_view(template_name='panel/crud/page_list.html'), name="content/page/list"),
    path('api/html/panel/content/page/update/<int:pk>', views.PanelPageUpdate.as_view(template_name='panel/crud/page_update.html'), name="content/page/update_IR"),
    path('api/html/panel/content/page/create', views.PanelPageCreate.as_view(template_name='panel/crud/page_create.html'), name="content/page/create"),
    path('api/html/panel/content/toast/list', views.PanelToastList.as_view(template_name='panel/crud/toast_list.html'), name="content/toast/list"),
    path('api/html/panel/content/toast/update/<int:pk>', views.PanelToastUpdate.as_view(template_name='panel/crud/toast_update.html'), name="content/toast/update_IR"),
    path('api/html/panel/content/toast/create', views.PanelToastCreate.as_view(template_name='panel/crud/toast_create.html'), name="content/toast/create"),
    path('api/html/panel/content/navbarlink/list', views.PanelNavbarLinkList.as_view(template_name='panel/crud/navbarlink_list.html'), name="content/navbarlink/list"),
    path('api/html/panel/content/navbarlink/update/<int:pk>', views.PanelNarbarLinkUpdate.as_view(template_name='panel/crud/navbarlink_update.html'), name="content/navbarlink/update_IR"),
    path('api/html/panel/content/navbarlink/create', views.PanelNarbarLinkCreate.as_view(template_name='panel/crud/navbarlink_create.html'), name="content/navbarlink/create"),
    path('api/html/panel/content/navbardropdown/list', views.PanelNavbarDropdownList.as_view(template_name='panel/crud/navbardropdown_list.html'), name="content/navbardropdown/list"),
    path('api/html/panel/content/navbardropdown/update/<int:pk>', views.PanelNavbarDropdownUpdate.as_view(template_name='panel/crud/navbardropdown_update.html'), name="content/navbardropdown/update_IR"),
    path('api/html/panel/content/navbardropdown/create', views.PanelNavbarDropdownCreate.as_view(template_name='panel/crud/navbardropdown_create.html'), name="content/navbardropdown/create"),
    path('api/html/panel/content/navwidget/list', views.PanelNavWidgetList.as_view(template_name='panel/crud/navwidget_list.html'), name="content/navwidget/list"),
    path('api/html/panel/content/navwidget/update/<int:pk>', views.PanelNavWidgetUpdate.as_view(template_name='panel/crud/navwidget_update.html'), name="content/navwidget/update_IR"),
    path('api/html/panel/content/navwidget/create', views.PanelNavWidgetCreate.as_view(template_name='panel/crud/navwidget_create.html'), name="content/navwidget/create"),
    path('api/html/panel/content/navwidgetbar/list', views.PanelNavWidgetBarList.as_view(template_name='panel/crud/navwidgetbar_list.html'), name="content/navwidgetbar/list"),
    path('api/html/panel/content/navwidgetbar/update/<int:pk>', views.PanelNavWidgetBarUpdate.as_view(template_name='panel/crud/navwidgetbar_update.html'), name="content/navwidgetbar/update_IR"),
    path('api/html/panel/content/navwidgetbar/create', views.PanelNavWidgetBarCreate.as_view(template_name='panel/crud/navwidgetbar_create.html'), name="content/navwidgetbar/create"),
    path('api/html/panel/bot/globalannouncement/list', views.PanelGlobalAnnouncementList.as_view(template_name='panel/crud/globalannouncement_list.html'), name="bot/globalannouncement/list"),
    path('api/html/panel/bot/globalannouncement/view/<int:pk>', views.PanelGlobalAnnouncementView.as_view(template_name='panel/crud/globalannouncement_view.html'), name="bot/globalannouncement/view_IR"),
    path('api/html/panel/bot/serverannouncement/list', views.PanelServerAnnouncementList.as_view(template_name='panel/crud/serverannouncement_list.html'), name="bot/serverannouncement/list"),
    path('api/html/panel/bot/serverannouncement/view/<int:pk>', views.PanelServerAnnouncementView.as_view(template_name='panel/crud/serverannouncement_view.html'), name="bot/serverannouncement/view_IR"),
    path('api/html/panel/bot/sentembedmessage/list', views.PanelSentEmbedMessageList.as_view(template_name='panel/crud/sentembedmessage_list.html'), name="bot/sentembedmessage/list"),
    path('api/html/panel/donations/donationpackage/list', views.PanelDonationPackageList.as_view(template_name='panel/crud/donationpackage_list.html'), name="donations/donationpackage/list"),
    path('api/html/panel/donations/donationpackage/update/<int:pk>', views.PanelDonationPackageUpdate.as_view(template_name='panel/crud/donationpackage_update.html'), name="donations/donationpackage/update_IR"),
    path('api/html/panel/donations/donationpackage/create', views.PanelDonationPackageCreate.as_view(template_name='panel/crud/donationpackage_create.html'), name="donations/donationpackage/create"),
    path('api/html/panel/donations/donationservercommand/list', views.PanelDonationServerCommandList.as_view(template_name='panel/crud/donationservercommand_list.html'), name="donations/donationservercommand/list"),
    path('api/html/panel/donations/donationservercommand/update/<int:pk>', views.PanelDonationServerCommandUpdate.as_view(template_name='panel/crud/donationservercommand_update.html'), name="donations/donationservercommand/update_IR"),
    path('api/html/panel/donations/donationservercommand/create', views.PanelDonationServerCommandCreate.as_view(template_name='panel/crud/donationservercommand_create.html'), name="donations/donationservercommand/create"),
    path('api/html/panel/donations/donationdiscordrole/list', views.PanelDonationDiscordRoleList.as_view(template_name='panel/crud/donationdiscordrole_list.html'), name="donations/donationdiscordrole/list"),
    path('api/html/panel/donations/donationdiscordrole/update/<int:pk>', views.PanelDonationDiscordRoleUpdate.as_view(template_name='panel/crud/donationdiscordrole_update.html'), name="donations/donationdiscordrole/update_IR"),
    path('api/html/panel/donations/donationdiscordrole/create', views.PanelDonationDiscordRoleCreate.as_view(template_name='panel/crud/donationdiscordrole_create.html'), name="donations/donationdiscordrole/create"),
    path('api/html/panel/donations/completeddonation/list', views.PanelCompletedDonationList.as_view(template_name='panel/crud/completeddonation_list.html'), name="donations/completeddonation/list"),
    path('api/html/panel/reporting', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/reporting/', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/settings', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/files/update', views.SettingsPanelFilePost.as_view(), name="settings_files_update"),
    path('api/html/panel/settings/defaultpages/update', views.SettingsPanelDefaultPagesPost.as_view(), name="settings_default_pages"),
    # Admin Panel Base View
    re_path(r'\S*', views.BaseView.as_view(), name='admin_panel_base'),

]

CURRENT_URLPATTERNS.append(urlpatterns)
