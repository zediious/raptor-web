# Generated by Django 4.2.7 on 2024-06-10 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("panel", "0003_panellogentry_action"),
    ]

    operations = [
        migrations.AlterField(
            model_name="panellogentry",
            name="changed_model",
            field=models.CharField(max_length=15000),
        ),
    ]
