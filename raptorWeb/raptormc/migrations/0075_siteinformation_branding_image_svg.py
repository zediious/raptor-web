# Generated by Django 4.2.7 on 2024-06-02 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("raptormc", "0074_siteinformation_query_delay"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteinformation",
            name="branding_image_svg",
            field=models.FileField(
                blank=True,
                help_text="The image displayed in the website Navigation Bar as a link to the homepage. This must be an SVG, and will override the webp Branding Image.",
                null=True,
                upload_to="branding_svg",
                verbose_name="Branding Image - SVG",
            ),
        ),
    ]