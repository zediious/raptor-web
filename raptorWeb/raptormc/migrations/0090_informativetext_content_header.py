# Generated by Django 4.2.7 on 2025-01-22 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0089_alter_siteinformation_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="informativetext",
            name="content_header",
            field=models.CharField(
                default="",
                help_text="If left blank, the default header will be used.",
                max_length=100,
                verbose_name="Header",
            ),
        ),
    ]
