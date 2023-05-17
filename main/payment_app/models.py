import datetime

from django.db import models
from django.utils import timezone


class Tariff(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название тарифа")
    description = models.TextField(verbose_name="Описание")
    old_price = models.IntegerField(verbose_name="Старая цена")
    new_price = models.IntegerField(verbose_name="Новая цена")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    type = models.ForeignKey(Tariff, verbose_name="Тариф курса", on_delete=models.CASCADE)
    lms_url = models.URLField(verbose_name="Ссылка на курс", max_length=1500)
    temporary_lms_url = models.URLField(verbose_name="Временная ссылка на курс", max_length=1500)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class PayboxSuccessPayment(models.Model):
    order_id = models.IntegerField


class PayboxSuccessPay(models.Model):
    payment_id = models.IntegerField(verbose_name='ID оплаты', unique=True)
    amount = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(max_length=3, verbose_name='Валюта')
    description = models.CharField(max_length=1000, verbose_name="Описание к оплате")
    payment_date = models.DateField(verbose_name='Дата оплаты', default=timezone.now)
    user_phone = models.CharField(verbose_name='Номер телефона', max_length=25)
    email = models.EmailField(verbose_name="Почта", max_length=255)
    signature = models.CharField(max_length=255, verbose_name="Подпись продукта", unique=True)
    order_id = models.IntegerField(verbose_name="ID Курса")
    type = models.CharField(max_length=255, verbose_name="Тариф")
    name = models.CharField(max_length=255, verbose_name="Название Курса")
    status = models.BooleanField(verbose_name="Статус оплаты", default=False)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return self.name


class TemporaryAccess(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    # email = models.EmailField(max_length=255, verbose_name="Email", unique=True)
    telegram_number = models.CharField(max_length=20, verbose_name='Телеграм номер', unique=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата начала доступа')

    class Meta:
        verbose_name = 'Временный доступ'
        verbose_name_plural = 'Временные доступы'

    def __str__(self):
        return self.name
