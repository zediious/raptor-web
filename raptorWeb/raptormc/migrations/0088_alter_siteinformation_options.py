# Generated by Django 4.2.7 on 2024-06-06 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0087_alter_siteinformation_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="siteinformation",
            options={
                "permissions": [
                    ("panel", "Can access the Control Panel Homepage"),
                    ("discord_bot", "Can access the Discord Bot control panel"),
                    ("discord_bot_panel", "Can access the Discord Bot control panel"),
                    (
                        "server_import_export",
                        "Can access the Server Import/Export menu",
                    ),
                    ("server_list", "Can access the list of created servers"),
                    ("server_create", "Can add new Servers."),
                    ("server_update", "Can edit the list of created servers"),
                    ("server_maintenance", "Can toggle a server's maintenance status."),
                    ("server_archive", "Can toggle a server's archive status."),
                    ("server_delete", "Can permanently delete a server."),
                    ("player_list", "Can access the list of Players."),
                    ("informativetext_view", "Can view the list of Informative Texts"),
                    ("informativetext_update", "Can update Informative Texts"),
                    ("page_list", "Can list Pages"),
                    ("page_update", "Can update Pages"),
                    ("page_add", "Can add Pages"),
                    ("page_delete", "Can delete Pages"),
                    ("toast_list", "Can list Toasts"),
                    ("toast_create", "Can create Toasts"),
                    ("toast_update", "Can update Toasts"),
                    ("toast_delete", "Can delete Toasts"),
                    ("navbarlinks_list", "Can list Navbar Links"),
                    ("navbarlinks_create", "Can create Navbar Links"),
                    ("navbarlinks_update", "Can update Navbar Links"),
                    ("navbarlinks_delete", "Can delete Navbar Links"),
                    ("globalannounce_list", "Can list Global Announcements"),
                    ("globalannounce_view", "Can view Global Announcements"),
                    ("globalannounce_update", "Can update Global Announcements"),
                    ("globalannounce_delete", "Can delete Global Announcements"),
                    ("serverannounce_list", "Can list Server Announcements"),
                    ("serverannounce_view", "Can view Server Announcements"),
                    ("serverannounce_update", "Can update Server Announcements"),
                    ("serverannounce_delete", "Can delete Server Announcements"),
                    ("donationpackage_list", "Can list Donation Packages"),
                    ("donationpackage_create", "Can create Donation Packages"),
                    ("donationpackage_update", "Can update Donation Packages"),
                    ("donationpackage_delete", "Can delete Donation Packages"),
                    ("donationservercommand_list", "Can list Donation Server Commands"),
                    (
                        "donationservercommand_create",
                        "Can create Donation Server Commands",
                    ),
                    (
                        "donationservercommand_update",
                        "Can update Donation Server Commands",
                    ),
                    (
                        "donationservercommand_delete",
                        "Can delete Donation Server Commands",
                    ),
                    ("donationdiscordrole_list", "Can list Donation Discord Roles"),
                    ("donationdiscordrole_create", "Can create Donation Discord Roles"),
                    ("donationdiscordrole_update", "Can update Donation Discord Roles"),
                    ("donationdiscordrole_delete", "Can delete Donation Discord Roles"),
                    ("completeddonation_list", "Can list Completed Donations"),
                    ("completeddonation_delete", "Can delete Completed Donations"),
                    (
                        "submittedstaffapplication_list",
                        "Can list Submitted Staff Applications",
                    ),
                    (
                        "submittedstaffapplication_view",
                        "Can view Submitted Staff Applications",
                    ),
                    (
                        "submittedstaffapplication_delete",
                        "Can view Submitted Staff Applications",
                    ),
                    (
                        "submittedstaffapplication_approval",
                        "Can approve or deny Submitted Staff Applications",
                    ),
                    (
                        "createdstaffapplication_list",
                        "Can list Created Staff Applications",
                    ),
                    (
                        "createdstaffapplication_create",
                        "Can create Created Staff Applications",
                    ),
                    (
                        "createdstaffapplication_update",
                        "Can update Created Staff Applications",
                    ),
                    (
                        "createdstaffapplication_delete",
                        "Can delete Created Staff Applications",
                    ),
                    ("staffapplicationfield_list", "Can list Staff Application Fields"),
                    (
                        "staffapplicationfield_create",
                        "Can create Staff Application Fields",
                    ),
                    (
                        "staffapplicationfield_update",
                        "Can update Staff Application Fields",
                    ),
                    (
                        "staffapplicationfield_delete",
                        "Can delete Staff Application Fields",
                    ),
                    ("reporting", "Can access Reporting"),
                    ("donations", "Can access Donations"),
                    ("settings", "Can access settings (DANGEROUS!)"),
                ],
                "verbose_name": ("Site Settings",),
                "verbose_name_plural": "Site Settings",
            },
        ),
    ]
