# Generated by Django 4.1.5 on 2023-02-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raptormc', '0011_alter_navbarlink_parent_dropdown'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationToast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The title of this notification that will appear on the website', max_length=100, verbose_name='Notification Name')),
                ('message', models.CharField(default='', help_text='The message for this notification', max_length=15000, verbose_name='Message')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
