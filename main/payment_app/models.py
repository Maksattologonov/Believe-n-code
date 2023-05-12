import datetime

from django.db import models
from django.utils import timezone
from decouple import config

from common.exceptions import IncorrectCodeException
from common.services import build_paybox_signature


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
    url = models.URLField(max_length=1000, verbose_name="Ссылки с Paybox оплаты")
    description = models.TextField(verbose_name="Описание")
    old_price = models.IntegerField(verbose_name="Старая цена")
    new_price = models.IntegerField(verbose_name="Новая цена")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            self.refresh_from_db()
            params = {
                'pg_order_id': self.id,
                'pg_merchant_id': int(config('PAYBOX_MERCHANT_ID')),
                'pg_amount': self.new_price,
                'pg_description': self.description,
                'pg_salt': f'Оплата за {self.name}, по тарифу {self.type}',
                'pg_result_url': str(config('PAYBOX_RESULT_URL')),
                'pg_testing_mode': int(config('PAYBOX_TESTING_MODE')),
                'pg_param1': self.name,
                'pg_param2': self.type.name
            }
            secret_key = str(config('PAYBOX_SECRET_KEY'))
            self.url = build_paybox_signature(params, secret_key)
            super().save(*args, **kwargs)
        except Exception as ex:
            raise IncorrectCodeException(ex)


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

