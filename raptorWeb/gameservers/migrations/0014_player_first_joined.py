# Generated by Django 4.2.7 on 2024-06-04 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gameservers", "0013_alter_server_modpack_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="first_joined",
            field=models.DateTimeField(
                auto_now_add=True, default='2024-06-04 00:00', verbose_name="First Joined Date"
            ),
            preserve_default=False,
        ),
    ]
