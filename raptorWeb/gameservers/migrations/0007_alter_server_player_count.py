# Generated by Django 4.2.7 on 2023-11-18 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameservers', '0006_alter_player_server_playercounthistoric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='player_count',
            field=models.IntegerField(default=0, help_text='The amount of players that were on this server the last time it was queried. Will always be zero if server querying is disabled.', verbose_name='Player Count'),
        ),
    ]
