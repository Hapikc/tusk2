# Generated by Django 5.1.4 on 2024-12-13 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_application_comment_application_design_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='application',
            name='design_image',
        ),
    ]