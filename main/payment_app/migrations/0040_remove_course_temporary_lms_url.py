# Generated by Django 4.2.1 on 2023-08-07 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0039_remove_tariff_new_price_remove_tariff_old_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='temporary_lms_url',
        ),
    ]
