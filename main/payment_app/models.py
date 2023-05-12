import datetime

from django.db import models
from django.utils import timezone


class Tariff(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название тарифа")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название курса")
    type = models.ForeignKey(Tariff, verbose_name="Тариф курса", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Описание")
    old_price = models.IntegerField(verbose_name="Старая цена")
    new_price = models.IntegerField(verbose_name="Новая цена")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class PayboxSuccessPayment(models.Model):
    order_id = models.IntegerField


class PayboxSuccessPay(models.Model):
    payment_id = models.IntegerField(verbose_name='ID оплаты')
    amount = models.IntegerField(verbose_name='Цена')
    currency = models.CharField(max_length=3, verbose_name='Валюта')
    description = models.CharField(max_length=100, verbose_name="Описание к оплате")
    payment_date = models.DateField(verbose_name='Дата оплаты', default=timezone.now)
    user_phone = models.CharField(verbose_name='Номер телефона', max_length=25)
    email = models.EmailField(verbose_name="Почта", max_length=255)
    signature = models.CharField(verbose_name="Подпись продукта")
    order_id = models.ForeignKey(Course, verbose_name="ID Курса", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, verbose_name="Тариф")
    name = models.CharField(max_length=255, verbose_name="Название Курса")

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return self.user_phone

