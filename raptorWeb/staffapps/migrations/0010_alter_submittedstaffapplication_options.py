# Generated by Django 4.2.7 on 2024-06-08 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("staffapps", "0009_submittedstaffapplication_approved"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="submittedstaffapplication",
            options={
                "permissions": [
                    (
                        "approval_submittedstaffapplication",
                        "Can approve or deny Submitted Staff Applications",
                    )
                ]
            },
        ),
    ]