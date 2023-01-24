# Generated by Django 3.2.5 on 2023-01-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameservers', '0002_server_discord_role_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='discord_role_id',
        ),
        migrations.AddField(
            model_name='server',
            name='discord_announcement_channel_id',
            field=models.CharField(default='None', max_length=200, verbose_name='Discord Announcment Channel ID'),
        ),
    ]