from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название тарифа")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тарифа")
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


class PayboxSuccessPayment(models.Model):
    order_id = models.IntegerField
