from django.db import models

from payment_app.models import Course, Tariff


class Mentor(models.Model):
    user_link = models.CharField(max_length=255, verbose_name="Ссылка на пользователя телеграм")
    direction = models.ForeignKey(Tariff, max_length=255, on_delete=models.CASCADE, verbose_name="Направление")

    def __str__(self):
        return self.user_link

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'


class TelegramGroup(models.Model):
    direction = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name="Ментор")
    type = models.ForeignKey(Course, max_length=255, on_delete=models.CASCADE, verbose_name="Курс")
    group_link = models.URLField(max_length=255, verbose_name="Ссылка на группу")

    def __str__(self):
        return self.group_link

    class Meta:
        verbose_name = 'Телеграм группа'
        verbose_name_plural = 'Телеграм группа'
