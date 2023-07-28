# Generated by Django 4.2.1 on 2023-07-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_app', '0026_telegramuser_delete_webinar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(default=3, max_length=100, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='country',
            field=models.CharField(choices=[('Bishkek', 'Бишкек'), ('Almaty', 'Алматы'), ('Tashkent', 'Ташкент'), ('Dushanbe', 'Душанбе'), ('Baku', 'Баку')], verbose_name='Страна'),
        ),
    ]
