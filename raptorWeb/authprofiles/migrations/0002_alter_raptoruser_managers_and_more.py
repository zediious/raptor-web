# Generated by Django 4.1.5 on 2023-02-09 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='raptoruser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='raptoruser',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Password Reset Token'),
        ),
    ]