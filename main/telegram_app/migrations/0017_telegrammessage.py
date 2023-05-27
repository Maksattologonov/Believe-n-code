# Generated by Django 4.2.1 on 2023-05-22 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_app', '0016_remove_mentor_telegram_username_mentor_user_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_id', models.IntegerField(verbose_name='ID телеграм бота')),
                ('text', models.TextField(verbose_name='Текст приветствия')),
                ('manager_id', models.IntegerField(verbose_name='ID менеджера')),
            ],
            options={
                'verbose_name': 'Сообщение телеграм бота',
            },
        ),
    ]