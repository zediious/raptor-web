# Generated by Django 4.2.7 on 2023-11-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raptormc', '0055_defaultpages_onboarding'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinformation',
            name='collapse_network_rules_when_accessing_server_rules',
            field=models.BooleanField(default=True, help_text='If this is un-checked, the Network Rules section on the Rules page will NOT be collapsed when accessing Rules from a Server Modal', verbose_name='Enable server querying and player counts section'),
        ),
    ]