# Generated by Django 4.2.7 on 2024-06-05 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0082_alter_page_page_css_alter_page_page_js"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="content",
            field=models.TextField(
                blank=True,
                default="",
                help_text="The content of this page.",
                max_length=15000,
                verbose_name="Content",
            ),
        ),
    ]
