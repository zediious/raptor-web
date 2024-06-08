# Generated by Django 4.2.7 on 2024-06-05 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0085_alter_notificationtoast_message"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="siteinformation",
            options={
                "permissions": [
                    ("panel", "Can access the Control Panel Homepage"),
                    ("discord_bot", "Can access the Discord Bot control panel"),
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
                    ("reporting", "Can access Reporting"),
                    ("donations", "Can access Donations"),
                    ("settings", "Can access settings (DANGEROUS!)"),
                ],
                "verbose_name": ("Site Settings",),
                "verbose_name_plural": "Site Settings",
            },
        ),
    ]
