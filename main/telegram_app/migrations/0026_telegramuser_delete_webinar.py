# Generated by Django 4.2.1 on 2023-07-28 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0033_webinar'),
        ('telegram_app', '0025_webinar'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True, verbose_name='ID пользователя')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Username')),
                ('phone_number', models.CharField(max_length=30, unique=True, verbose_name='Номер телефона')),
                ('country', models.CharField(choices=[('KG', 'Kyrgyzstan'), ('UZ', 'Uzbekistan'), ('KZ', 'Kazakhstan'), ('RU', 'Russia'), ('TJ', 'Tajikistan')], verbose_name='Страна')),
                ('webinar', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payment_app.webinar', verbose_name='Вебинар')),
            ],
            options={
                'verbose_name': 'Пользователи телеграм',
                'verbose_name_plural': 'Пользователи телеграм',
            },
        ),
        migrations.DeleteModel(
            name='Webinar',
        ),
    ]
