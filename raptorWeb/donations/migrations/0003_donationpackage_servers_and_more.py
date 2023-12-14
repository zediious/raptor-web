# Generated by Django 4.2.7 on 2023-12-10 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameservers', '0012_alter_server_rcon_address_alter_server_rcon_password_and_more'),
        ('donations', '0002_donationpackage_package_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationpackage',
            name='servers',
            field=models.ManyToManyField(to='gameservers.server', verbose_name='Servers to send Commands to.'),
        ),
        migrations.AlterField(
            model_name='donationpackage',
            name='commands',
            field=models.ManyToManyField(to='donations.donationservercommand', verbose_name='Commands to Send.'),
        ),
    ]
