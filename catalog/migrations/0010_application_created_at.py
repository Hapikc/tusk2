# Generated by Django 5.1.4 on 2024-12-12 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_application_user_alter_application_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]