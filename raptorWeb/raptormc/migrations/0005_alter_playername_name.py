# Generated by Django 3.2.5 on 2022-08-18 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raptormc', '0004_auto_20220818_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playername',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]