# Generated by Django 4.2.7 on 2024-05-28 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authprofiles', '0006_userprofileinfo_hidden_from_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='raptoruser',
            name='date_queued_for_delete',
            field=models.DateTimeField(blank=True, default=None, verbose_name='Date Queued for Deletion'),
        ),
    ]
