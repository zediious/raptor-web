from django.urls import URLPattern, path, re_path

from raptorWeb.panel import views
from raptorWeb.panel.routes import CURRENT_URLPATTERNS

app_name: str = "panel"

urlpatterns: list[URLPattern] = [

    # Panel Homepage
    path('api/html/panel/home', views.HomePanel.as_view(), name="home"),
    path('api/html/panel/home/', views.HomePanel.as_view(), name="home"),
    # Discord Bot Control Panel
    path('api/html/panel/discordbot', views.DiscordBotPanel.as_view(), name="discordbot"),
    path('api/html/panel/discordbot/', views.DiscordBotPanel.as_view(), name="discordbot"),
    # Panel Log Entry
    path('api/html/panel/logentry/list', views.PanelLogEntryList.as_view(), name="logentry/list"),
    # Server
    path('api/html/panel/reporting', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/reporting/', views.ReportingPanel.as_view(), name="reporting"),
    path('api/html/panel/server/importexport', views.ServerActionsPanel.as_view(), name="server/importexport"),
    path('api/html/panel/server/importexport/', views.ServerActionsPanel.as_view(), name="server/importexport"),
    path('api/html/panel/server/list/', views.PanelServerList.as_view(), name="server/list"),
    path('api/html/panel/server/archivedlist', views.PanelServerList.as_view(template_name='panel/crud/server_list_archived.html'), name="server/archivedlist"),
    path('api/html/panel/server/update/<int:pk>', views.PanelServerUpdate.as_view(), name="server/update_IR"),
    path('api/html/panel/server/create', views.PanelServerCreate.as_view(), name="server/create"),
    path('api/html/panel/server/delete', views.PanelServerDelete.as_view(), name="server/delete"),
    # Player
    path('api/html/panel/player/list', views.PanelPlayerList.as_view(), name="player/list"),
    # Informative Text
    path('api/html/panel/content/informativetext/list', views.PanelInformativeTextList.as_view(), name="content/informativetext/list"),
    path('api/html/panel/content/informativetext/update/<int:pk>', views.PanelInformativeTextUpdate.as_view(), name="content/informativetext/update_IR"),
    # Page
    path('api/html/panel/content/page/list', views.PanelPageList.as_view(), name="content/page/list"),
    path('api/html/panel/content/page/update/<int:pk>', views.PanelPageUpdate.as_view(), name="content/page/update_IR"),
    path('api/html/panel/content/page/create', views.PanelPageCreate.as_view(), name="content/page/create"),
    path('api/html/panel/content/page/delete', views.PanelPageDelete.as_view(), name="content/page/delete"),
    # Toast
    path('api/html/panel/content/toast/list', views.PanelToastList.as_view(), name="content/toast/list"),
    path('api/html/panel/content/toast/update/<int:pk>', views.PanelToastUpdate.as_view(), name="content/toast/update_IR"),
    path('api/html/panel/content/toast/create', views.PanelToastCreate.as_view(), name="content/toast/create"),
    path('api/html/panel/content/toast/delete', views.PanelToastDelete.as_view(), name="content/toast/delete"),
    # Navbar Link
    path('api/html/panel/content/navbarlink/list', views.PanelNavbarLinkList.as_view(), name="content/navbarlink/list"),
    path('api/html/panel/content/navbarlink/update/<int:pk>', views.PanelNarbarLinkUpdate.as_view(), name="content/navbarlink/update_IR"),
    path('api/html/panel/content/navbarlink/create', views.PanelNarbarLinkCreate.as_view(), name="content/navbarlink/create"),
    path('api/html/panel/content/navbarlink/delete', views.PanelNavbarLinkDelete.as_view(), name="content/navbarlink/delete"),
    # Navbar Dropdown
    path('api/html/panel/content/navbardropdown/list', views.PanelNavbarDropdownList.as_view(), name="content/navbardropdown/list"),
    path('api/html/panel/content/navbardropdown/update/<int:pk>', views.PanelNavbarDropdownUpdate.as_view(), name="content/navbardropdown/update_IR"),
    path('api/html/panel/content/navbardropdown/create', views.PanelNavbarDropdownCreate.as_view(), name="content/navbardropdown/create"),
    path('api/html/panel/content/navbardropdown/delete', views.PanelNavbarDropdownDelete.as_view(), name="content/navbardropdown/delete"),
    # Nav Widget
    path('api/html/panel/content/navwidget/list', views.PanelNavWidgetList.as_view(), name="content/navwidget/list"),
    path('api/html/panel/content/navwidget/update/<int:pk>', views.PanelNavWidgetUpdate.as_view(), name="content/navwidget/update_IR"),
    path('api/html/panel/content/navwidget/create', views.PanelNavWidgetCreate.as_view(), name="content/navwidget/create"),
    path('api/html/panel/content/navwidget/delete', views.PanelNavWidgetDelete.as_view(), name="content/navwidget/delete"),
    # Nav Widget Bar
    path('api/html/panel/content/navwidgetbar/list', views.PanelNavWidgetBarList.as_view(), name="content/navwidgetbar/list"),
    path('api/html/panel/content/navwidgetbar/update/<int:pk>', views.PanelNavWidgetBarUpdate.as_view(), name="content/navwidgetbar/update_IR"),
    path('api/html/panel/content/navwidgetbar/create', views.PanelNavWidgetBarCreate.as_view(), name="content/navwidgetbar/create"),
    path('api/html/panel/content/navwidgetbar/delete', views.PanelNavWidgetBarDelete.as_view(), name="content/navwidgetbar/delete"),
    # Global Announcement
    path('api/html/panel/bot/globalannouncement/list', views.PanelGlobalAnnouncementList.as_view(), name="bot/globalannouncement/list"),
    path('api/html/panel/bot/globalannouncement/view/<int:pk>', views.PanelGlobalAnnouncementView.as_view(), name="bot/globalannouncement/view_IR"),
    path('api/html/panel/bot/globalannouncement/delete', views.PanelGlobalAnnouncementDelete.as_view(), name="bot/globalannouncement/delete"),
    # Server Announcement
    path('api/html/panel/bot/serverannouncement/list', views.PanelServerAnnouncementList.as_view(), name="bot/serverannouncement/list"),
    path('api/html/panel/bot/serverannouncement/view/<int:pk>', views.PanelServerAnnouncementView.as_view(), name="bot/serverannouncement/view_IR"),
    path('api/html/panel/bot/serverannouncement/delete', views.PanelServerAnnouncementDelete.as_view(), name="bot/serverannouncement/delete"),
    # Sent Embed Message
    path('api/html/panel/bot/sentembedmessage/list', views.PanelSentEmbedMessageList.as_view(), name="bot/sentembedmessage/list"),
    path('api/html/panel/bot/sentembedmessage/delete', views.PanelSentEmbedMessageDelete.as_view(), name="bot/sentembedmessage/delete"),
    # Donation Package
    path('api/html/panel/donations/donationpackage/list', views.PanelDonationPackageList.as_view(), name="donations/donationpackage/list"),
    path('api/html/panel/donations/donationpackage/update/<int:pk>', views.PanelDonationPackageUpdate.as_view(), name="donations/donationpackage/update_IR"),
    path('api/html/panel/donations/donationpackage/create', views.PanelDonationPackageCreate.as_view(), name="donations/donationpackage/create"),
    path('api/html/panel/donations/donationpackage/delete', views.PanelDonationPackageDelete.as_view(), name="donations/donationpackage/delete"),
    # Donation Server Command
    path('api/html/panel/donations/donationservercommand/list', views.PanelDonationServerCommandList.as_view(), name="donations/donationservercommand/list"),
    path('api/html/panel/donations/donationservercommand/update/<int:pk>', views.PanelDonationServerCommandUpdate.as_view(), name="donations/donationservercommand/update_IR"),
    path('api/html/panel/donations/donationservercommand/create', views.PanelDonationServerCommandCreate.as_view(), name="donations/donationservercommand/create"),
    path('api/html/panel/donations/donationservercommand/delete', views.PanelDonationServerCommandDelete.as_view(), name="donations/donationservercommand/delete"),
    # Donation Discord Role
    path('api/html/panel/donations/donationdiscordrole/list', views.PanelDonationDiscordRoleList.as_view(), name="donations/donationdiscordrole/list"),
    path('api/html/panel/donations/donationdiscordrole/update/<int:pk>', views.PanelDonationDiscordRoleUpdate.as_view(), name="donations/donationdiscordrole/update_IR"),
    path('api/html/panel/donations/donationdiscordrole/create', views.PanelDonationDiscordRoleCreate.as_view(), name="donations/donationdiscordrole/create"),
    path('api/html/panel/donations/donationdiscordrole/delete', views.PanelDonationDiscordRoleDelete.as_view(), name="donations/donationdiscordrole/delete"),
    # Completed Donation
    path('api/html/panel/donations/completeddonation/list', views.PanelCompletedDonationList.as_view(), name="donations/completeddonation/list"),
    path('api/html/panel/donations/completeddonation/delete', views.PanelCompletedDonationDelete.as_view(), name="donations/completeddonation/delete"),
    # Submitted Staff Application
    path('api/html/panel/staffapps/submittedstaffapplication/list', views.PanelSubmittedStaffApplicationList.as_view(), name="staffapps/submittedstaffapplication/list"),
    path('api/html/panel/staffapps/submittedstaffapplication/view/<int:pk>', views.PanelSubmittedStaffApplicationView.as_view(), name="staffapps/submittedstaffapplication/view_IR"),
    path('api/html/panel/staffapps/submittedstaffapplication/delete', views.PanelSubmittedStaffApplicationDelete.as_view(), name="staffapps/submittedstaffapplication/delete"),
    # Created Staff Application
    path('api/html/panel/staffapps/createdstaffapplication/list', views.PanelCreatedStaffApplicationList.as_view(), name="staffapps/createdstaffapplication/list"),
    path('api/html/panel/staffapps/createdstaffapplication/update/<int:pk>', views.PanelCreatedStaffApplicationUpdate.as_view(), name="staffapps/createdstaffapplication/update_IR"),
    path('api/html/panel/staffapps/createdstaffapplication/create', views.PanelCreatedStaffApplicationCreate.as_view(), name="staffapps/createdstaffapplication/create"),
    path('api/html/panel/staffapps/createdstaffapplication/delete', views.PanelCreatedStaffApplicationDelete.as_view(), name="staffapps/createdstaffapplication/delete"),
    # Staff Application Field
    path('api/html/panel/staffapps/staffapplicationfield/list', views.PanelStaffApplicationFieldList.as_view(), name="staffapps/staffapplicationfield/list"),
    path('api/html/panel/staffapps/staffapplicationfield/update/<int:pk>', views.PanelStaffApplicationFieldUpdate.as_view(), name="staffapps/staffapplicationfield/update_IR"),
    path('api/html/panel/staffapps/staffapplicationfield/create', views.PanelStaffApplicationFieldCreate.as_view(), name="staffapps/staffapplicationfield/create"),
    path('api/html/panel/staffapps/staffapplicationfield/delete', views.PanelStaffApplicationFieldDelete.as_view(), name="staffapps/staffapplicationfield/delete"),
    # Raptor User
    path('api/html/panel/users/raptoruser/list', views.PanelUserList.as_view(), name="users/raptoruser/list"),
    path('api/html/panel/users/raptoruser/update/<int:pk>', views.PanelUserUpdate.as_view(), name="users/raptoruser/update_IR"),
    path('api/html/panel/users/userprofileinfo/update/<int:pk>', views.PanelUserProfileInfoUpdate.as_view(), name="users/userprofileinfo/update_IR"),
    path('api/html/panel/users/discorduserinfo/update/<int:pk>', views.PanelDiscordUserInfoUpdate.as_view(), name="users/discorduserinfo/update_IR"),
    path('api/html/panel/users/raptoruser/delete', views.PanelUserDelete.as_view(), name="users/raptoruser/delete"),
    # Raptor User Group
    path('api/html/panel/users/raptorusergroup/list', views.PanelRaptorUserGroupList.as_view(), name="users/raptorusergroup/list"),
    path('api/html/panel/users/raptorusergroup/update/<int:pk>', views.PanelRaptorUserGroupUpdate.as_view(), name="users/raptorusergroup/update_IR"),
    path('api/html/panel/users/raptorusergroup/create', views.PanelRaptorUserGroupCreate.as_view(), name="users/raptorusergroup/create"),
    path('api/html/panel/users/raptorusergroup/delete', views.PanelRaptorUserGroupDelete.as_view(), name="users/raptorusergroup/delete"),
    # Deletion Queue For User
    path('api/html/panel/users/deletionqueue/list', views.PanelDeletionQueueForUserList.as_view(), name="users/deletionqueue/list"),
    path('api/html/panel/users/deletionqueue/delete', views.PanelDeletionQueueForUserDelete.as_view(), name="users/deletionqueue/delete"),
    # Site Settings
    path('api/html/panel/settings', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/', views.SettingsPanel.as_view(), name="settings"),
    path('api/html/panel/settings/files/update', views.SettingsPanelFilePost.as_view(), name="settings_files_update"),
    path('api/html/panel/settings/defaultpages/update', views.SettingsPanelDefaultPagesPost.as_view(), name="settings_default_pages"),
    # Admin Panel Base View
    re_path(r'\S*', views.BaseView.as_view(), name='admin_panel_base'),

]

CURRENT_URLPATTERNS.append(urlpatterns)
