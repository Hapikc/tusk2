# Generated by Django 5.1.4 on 2024-12-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_application_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
