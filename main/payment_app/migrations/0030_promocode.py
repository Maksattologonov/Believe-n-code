# Generated by Django 4.2.1 on 2023-07-18 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0029_alter_payboxsuccesspay_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимум 20 символов', max_length=20, unique=True, verbose_name='Промокод')),
                ('date_of', models.DateField(default=datetime.datetime(2023, 7, 18, 6, 40, 15, 81678, tzinfo=datetime.timezone.utc), verbose_name='Дата действия промокода')),
            ],
            options={
                'verbose_name': 'Паромокод',
                'verbose_name_plural': 'Паромокоды',
            },
        ),
    ]
