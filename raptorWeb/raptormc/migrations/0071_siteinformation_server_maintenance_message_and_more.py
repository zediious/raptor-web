# Generated by Django 4.2.7 on 2024-04-25 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0070_siteinformation_paypal_enabled_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteinformation",
            name="server_maintenance_message",
            field=models.CharField(
                default="Server is in maintenance mode!",
                help_text="Text shown in tooltip while hovering over a server in Maintenance Mode's status icon.",
                max_length=500,
                verbose_name="Server Maintenace Message",
            ),
        ),
        migrations.AddField(
            model_name="siteinformation",
            name="server_offline_message",
            field=models.CharField(
                default="Server is offline!",
                help_text="Text shown in tooltip while hovering over an offline server status icon.",
                max_length=500,
                verbose_name="Server Offline Message",
            ),
        ),
        migrations.AddField(
            model_name="siteinformation",
            name="server_online_message",
            field=models.CharField(
                default="Server is online!",
                help_text="Text shown in tooltip while hovering over an online server status icon.",
                max_length=500,
                verbose_name="Server Online Message",
            ),
        ),
    ]