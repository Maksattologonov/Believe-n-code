# Generated by Django 4.2 on 2023-04-30 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_app', '0005_telegramusers_alter_mentor_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TelegramUsers',
            new_name='TelegramUser',
        ),
    ]
