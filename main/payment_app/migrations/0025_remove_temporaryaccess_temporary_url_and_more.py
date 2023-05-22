# Generated by Django 4.2.1 on 2023-05-16 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_app', '0024_temporaryaccess_temporary_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temporaryaccess',
            name='temporary_url',
        ),
        migrations.AddField(
            model_name='course',
            name='temporary_lms_url',
            field=models.URLField(default=1, max_length=1500, verbose_name='Временная ссылка на курс'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryaccess',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment_app.course', verbose_name='Курс'),
            preserve_default=False,
        ),
    ]
