# Generated by Django 4.2.7 on 2024-06-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffapps", "0002_adminapplication_approved_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffApplicationField",
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
                    "name",
                    models.CharField(
                        help_text="The name of this field",
                        max_length=500,
                        verbose_name="Field Name",
                    ),
                ),
                (
                    "help_text",
                    models.CharField(
                        help_text="The help text of this field",
                        max_length=500,
                        verbose_name="Help Text",
                    ),
                ),
                (
                    "widget",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("int", "Number"),
                            ("bool", "Yes or No"),
                        ],
                        default="text",
                        help_text="The widget type used for this form",
                        max_length=5,
                        verbose_name="Form Widget",
                    ),
                ),
            ],
        ),
    ]
