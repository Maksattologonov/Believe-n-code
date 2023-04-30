from django.db import models


class Tariff(models.Model):
    COURSES = [
        ("Front-end", "Front-end"),
        ("Back-end", "Back-end"),
        ("Design", "Design")]
    name = models.CharField(max_length=255, verbose_name="Название тарифа")
    type = models.CharField(max_length=50, choices=COURSES, verbose_name="Тип курса")
    description = models.TextField(verbose_name="Описание")
    old_price = models.IntegerField(verbose_name="Старая цена")
    new_price = models.IntegerField(verbose_name="Новая цена")

    def __str__(self):
        return self.name


class PayboxUrl(models.Model):
    COURSES = [
        ("Up", "Up"),
        ("Pro", "Pro"),
        ("Ultra", "Ultra")]
    url = models.URLField(max_length=1000, verbose_name="Ссылки с Paybox оплаты")
    type_of = models.CharField(max_length=20, choices=COURSES)

    def __str__(self):
        return self.type_of
