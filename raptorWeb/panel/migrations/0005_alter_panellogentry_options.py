# Generated by Django 4.2.7 on 2024-07-14 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("panel", "0004_alter_panellogentry_changed_model"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="panellogentry",
            options={"verbose_name": "Change List", "verbose_name_plural": "Changes"},
        ),
    ]
