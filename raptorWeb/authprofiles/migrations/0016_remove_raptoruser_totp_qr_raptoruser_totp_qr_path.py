# Generated by Django 4.2.7 on 2024-05-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authprofiles", "0015_raptoruser_totp_qr"),
    ]

    operations = [
        migrations.RemoveField(model_name="raptoruser", name="totp_qr",),
        migrations.AddField(
            model_name="raptoruser",
            name="totp_qr_path",
            field=models.CharField(
                blank=True,
                max_length=500,
                null=True,
                verbose_name="TOT QR Image Filename",
            ),
        ),
    ]
