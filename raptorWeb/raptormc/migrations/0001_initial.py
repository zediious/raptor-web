# Generated by Django 3.2.5 on 2022-10-21 23:24

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=500, verbose_name='Position applied for')),
                ('age', models.IntegerField(verbose_name='Applicant age')),
                ('time', models.CharField(max_length=500, verbose_name='Time Zone and alottable time')),
                ('mc_name', models.CharField(max_length=500, verbose_name='Minecraft Username')),
                ('discord_name', models.CharField(max_length=500, verbose_name='Discord Username/ID')),
                ('voice_chat', models.BooleanField(max_length=500, verbose_name='Capable of using Voice Chat?')),
                ('description', models.TextField(max_length=500, verbose_name='General self-description')),
                ('modpacks', models.TextField(max_length=500, verbose_name='Knowledge of server modpacks/general Modded Minecraft')),
                ('plugins', models.TextField(max_length=500, verbose_name='Knowledge of plugins/server mods and adaptability')),
                ('api', models.TextField(max_length=500, verbose_name='Knowledge of server APIs and Minecraft proxies.')),
                ('IT_knowledge', models.TextField(max_length=500, verbose_name="IT/Software/Networking knowledge, as well as whether one's work involves these topics.")),
                ('linux', models.TextField(max_length=500, verbose_name='Knowledge in Linux System Administration and CLI use.')),
                ('ptero', models.TextField(max_length=500, verbose_name='Knowledge of Pterodactyl Panel')),
                ('experience', models.TextField(max_length=500, verbose_name='Experience on other servers')),
                ('why_join', models.TextField(max_length=500, verbose_name='Reasons for wanting to be staff.')),
            ],
            options={
                'verbose_name': 'Admin Application',
                'verbose_name_plural': 'Admin Applications',
            },
        ),
        migrations.CreateModel(
            name='InformativeText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('name', models.CharField(default='Default', max_length=50, verbose_name='Content Name')),
                ('content', ckeditor.fields.RichTextField(default='', max_length=15000, verbose_name='Content')),
            ],
            options={
                'verbose_name': ('Informative Text',),
                'verbose_name_plural': 'Informative Texts',
            },
        ),
        migrations.CreateModel(
            name='ModeratorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=500, verbose_name='Position applied for')),
                ('age', models.IntegerField(verbose_name='Applicant age')),
                ('time', models.CharField(max_length=500, verbose_name='Time Zone and alottable time')),
                ('mc_name', models.CharField(max_length=500, verbose_name='Minecraft Username')),
                ('discord_name', models.CharField(max_length=500, verbose_name='Discord Username/ID')),
                ('voice_chat', models.BooleanField(max_length=500, verbose_name='Capable of Voice Chat?')),
                ('contact_uppers', models.TextField(max_length=500, verbose_name='Ability to reach higher-ups')),
                ('description', models.TextField(max_length=50, verbose_name='General self-description')),
                ('modpacks', models.TextField(max_length=500, verbose_name='Knowledge of server modpacks/general Modded Minecraft')),
                ('experience', models.TextField(max_length=500, verbose_name='Experience on other servers')),
                ('why_join', models.TextField(max_length=500, verbose_name='Reasons for wanting to be stff')),
            ],
            options={
                'verbose_name': 'Moderator Application',
                'verbose_name_plural': 'Moderator Applications',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_state', models.BooleanField(default=False)),
                ('in_maintenance', models.BooleanField(default=False, verbose_name='Maintenance Mode')),
                ('server_address', models.CharField(max_length=50)),
                ('modpack_name', models.CharField(default='Unnamed Modpack', max_length=100, verbose_name='Modpack Name')),
                ('modpack_description', ckeditor.fields.RichTextField(default='Modpack Description', max_length=1500, verbose_name='Modpack Description')),
                ('server_description', ckeditor.fields.RichTextField(default='Server Description', max_length=1500, verbose_name='Server Description')),
                ('server_rules', ckeditor.fields.RichTextField(default='Server-specific Rules', max_length=1500, verbose_name='Server-Specific Rules')),
                ('server_banned_items', ckeditor.fields.RichTextField(default='Server-specific Banned Items', max_length=1500, verbose_name='Server-specific Banned Items')),
                ('server_vote_links', ckeditor.fields.RichTextField(default='Server-specific Vote Links', max_length=1500, verbose_name='Voting Site Links')),
                ('modpack_url', models.URLField(verbose_name='Link to Modpack')),
            ],
            options={
                'verbose_name': 'Server',
                'verbose_name_plural': 'Servers',
            },
        ),
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('minecraft_username', models.CharField(max_length=50)),
                ('discord_username', models.CharField(blank=True, max_length=50)),
                ('favorite_modpack', models.CharField(blank=True, max_length=80)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User - Extra Information',
                'verbose_name_plural': 'Users - Extra Information',
            },
        ),
        migrations.CreateModel(
            name='PlayerName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('server', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='raptormc.server')),
            ],
            options={
                'verbose_name': 'Player Name',
                'verbose_name_plural': 'Player Names',
            },
        ),
        migrations.CreateModel(
            name='PlayerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_count', models.IntegerField(default=0)),
                ('server', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='raptormc.server')),
            ],
            options={
                'verbose_name': 'Player Count',
                'verbose_name_plural': 'Player Counts',
            },
        ),
    ]
