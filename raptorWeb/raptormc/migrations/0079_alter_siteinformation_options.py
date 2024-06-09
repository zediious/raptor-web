# Generated by Django 4.2.7 on 2024-06-05 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0078_alter_siteinformation_options"),
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
                    ("server_update", "Can edit the list of created servers"),
                    ("server_maintenance", "Can toggle a server's maintenance status."),
                    ("server_archive", "Can toggle a server's archive status."),
                    ("server_delete", "Can permanently delete a server."),
                    ("player_list", "Can access the list of Players."),
                    ("informativetext_view", "Can view the list of Informative Texts"),
                    ("informativetext_update", "Can update Informative Texts"),
                    ("reporting", "Can access Reporting"),
                    ("donations", "Can access Donations"),
                    ("settings", "Can access settings (DANGEROUS!)"),
                ],
                "verbose_name": ("Site Settings",),
                "verbose_name_plural": "Site Settings",
            },
        ),
    ]
