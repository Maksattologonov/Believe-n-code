# Generated by Django 4.2.1 on 2023-05-27 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0029_alter_payboxsuccesspay_description'),
        ('telegram_app', '0022_telegrambot_alter_installmenttelegram_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='direction',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, to='payment_app.course', verbose_name='Направление'),
        ),
    ]
