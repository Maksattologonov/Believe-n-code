from django.db import models

from django.utils import timezone
from payment_app.models import Course, Tariff

from payment_app.models import Webinar


class TelegramBot(models.Model):
    bot_link = models.URLField(max_length=100, verbose_name='Ссылка на бота', help_text='пример: https://t.me/TEST_BOT')

    def __str__(self):
        return self.bot_link

    class Meta:
        verbose_name = 'Телеграм бот'
        verbose_name_plural = 'Телеграм бот'

    def save(self, *args, **kwargs):
        if not self.pk and TelegramBot.objects.exists():
            return TelegramBot.objects.update_or_create(*args, **kwargs)
        return super(TelegramBot, self).save(*args, **kwargs)


class Mentor(models.Model):
    user_link = models.CharField(max_length=255, verbose_name="Ссылка на пользователя телеграм")
    direction = models.ForeignKey(Course, max_length=255, on_delete=models.CASCADE, verbose_name="Направление")

    def __str__(self):
        return self.user_link

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'


class TelegramGroup(models.Model):
    direction = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name="Ментор")
    type = models.ForeignKey(Course, max_length=255, on_delete=models.CASCADE, verbose_name="Курс")
    group_link = models.URLField(max_length=255, verbose_name="Ссылка на группу")
    text = models.TextField(verbose_name="Текст приветствия")

    def __str__(self):
        return self.group_link

    class Meta:
        verbose_name = 'Сообщение при добавлении в группу'
        verbose_name_plural = 'Сообщение при добавлении в группу'


class TelegramMessage(models.Model):
    text = models.TextField(verbose_name="Текст приветствия")
    manager_id = models.CharField(max_length=50, verbose_name="Телеграм ID менеджера")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение при добавлении'
        verbose_name_plural = 'Сообщение при добавлении'

    def save(self, *args, **kwargs):
        if not self.pk and TelegramMessage.objects.exists():
            return TelegramMessage.objects.update_or_create(*args, **kwargs)
        return super(TelegramMessage, self).save(*args, **kwargs)


class ContactUsTelegram(models.Model):
    text = models.TextField(verbose_name="Текст")
    manager_id = models.CharField(max_length=50, verbose_name='Телеграм ID менеджера')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Сообщение связаться с нами'
        verbose_name_plural = 'Сообщение связаться с нами'

    def save(self, *args, **kwargs):
        if not self.pk and ContactUsTelegram.objects.exists():
            return ContactUsTelegram.objects.update_or_create(*args, **kwargs)
        return super(ContactUsTelegram, self).save(*args, **kwargs)


class InstallmentTelegram(models.Model):
    text = models.TextField(verbose_name="Текст для программы рассрочки")
    manager_id = models.CharField(max_length=50, verbose_name='Телеграм ID менеджера')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Программа рассрочки'
        verbose_name_plural = 'Программа рассрочки'

    def save(self, *args, **kwargs):
        if not self.pk and InstallmentTelegram.objects.exists():
            return InstallmentTelegram.objects.update_or_create(*args, **kwargs)
        return super(InstallmentTelegram, self).save(*args, **kwargs)


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(verbose_name='ID пользователя', unique=True)
    username = models.CharField(verbose_name='Username', max_length=100, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=100)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    location = models.CharField(max_length=255, verbose_name='Часовой пояс')
    webinar = models.ForeignKey(Webinar, on_delete=models.DO_NOTHING, verbose_name='Вебинар')

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'Пользователи телеграм'
        verbose_name_plural = 'Пользователи телеграм'


class TelegramAdmin(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True, verbose_name="Телеграм ID")

    class Meta:
        verbose_name = 'Администратор Telegram'
        verbose_name_plural = 'Администраторы Telegram'

    def __str__(self):
        return str(self.id)
