# Generated by Django 5.1.4 on 2024-12-11 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_advuser_consent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advuser',
            name='consent',
        ),
    ]
