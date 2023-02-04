# Generated by Django 4.1.5 on 2023-02-04 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authprofiles", "0010_alter_raptoruser_discord_user_info_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="discorduserinfo",
            name="avatar_string",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="userprofileinfo",
            name="picture_changed_manually",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
