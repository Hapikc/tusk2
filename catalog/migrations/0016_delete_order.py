# Generated by Django 5.1.4 on 2024-12-12 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
