# Generated by Django 4.1.5 on 2023-01-26 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authprofiles', '0007_alter_discorduserinfo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='raptoruser',
            name='is_discord_user',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
