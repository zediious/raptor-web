# Generated by Django 4.2.7 on 2024-06-06 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffapps", "0004_createdstaffapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="createdstaffapplication",
            name="name",
            field=models.CharField(
                default="Default",
                help_text="The name of this Staff Application and/or the position being applied for",
                max_length=500,
                verbose_name="Staff Application Name",
            ),
        ),
    ]