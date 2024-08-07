# Generated by Django 4.2.7 on 2024-07-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staffapps", "0011_alter_createdstaffapplication_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffapplicationfield",
            name="widget",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("large_text", "Large Text"),
                    ("int", "Number"),
                    ("bool", "Yes or No"),
                ],
                default="text",
                help_text="The widget type used for this form",
                max_length=10,
                verbose_name="Form Widget",
            ),
        ),
    ]
