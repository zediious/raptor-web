# Generated by Django 4.2.7 on 2024-06-06 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffapps", "0005_createdstaffapplication_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubmittedStaffApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "submitted_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="JSON data representing the submitted form fields",
                        null=True,
                        verbose_name="Submitted Data",
                    ),
                ),
            ],
        ),
    ]
