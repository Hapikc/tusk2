# Generated by Django 5.1.4 on 2024-12-12 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_remove_application_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]