# Generated by Django 4.1.5 on 2023-01-26 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authprofiles', '0003_remove_discorduserinfo_favorite_modpack_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raptoruser',
            name='discord_user_info',
        ),
        migrations.RemoveField(
            model_name='raptoruser',
            name='user_profile_info',
        ),
        migrations.AddField(
            model_name='discorduserinfo',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authprofiles.raptoruser'),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authprofiles.raptoruser'),
        ),
    ]
