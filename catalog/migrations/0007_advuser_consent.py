# Generated by Django 5.1.4 on 2024-12-11 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_advuser_consent'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='consent',
            field=models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных'),
        ),
    ]
