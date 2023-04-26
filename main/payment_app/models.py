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

