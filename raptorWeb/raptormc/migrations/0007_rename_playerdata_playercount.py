# Generated by Django 3.2.5 on 2022-08-18 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raptormc', '0006_alter_playername_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlayerData',
            new_name='PlayerCount',
        ),
    ]
