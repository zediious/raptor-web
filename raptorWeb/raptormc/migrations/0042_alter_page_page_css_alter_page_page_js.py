# Generated by Django 4.2.5 on 2023-10-07 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raptormc', '0041_alter_page_page_css_alter_page_page_js'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_css',
            field=models.FileField(blank=True, help_text='Custom style sheet that will only apply on this page. This will apply only to this page, overriding any defaults.', upload_to='page_css', verbose_name='Page CSS'),
        ),
        migrations.AlterField(
            model_name='page',
            name='page_js',
            field=models.FileField(blank=True, help_text='Custom Javascript that will only apply on this page.', upload_to='page_js', verbose_name='Page JavaScript'),
        ),
    ]
