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


class Mentor(models.Model):
    COURSES = [
        ("Front-end", "Front-end"),
        ("Back-end", "Back-end"),
        ("Design", "Design")]
    telegram_username = models.CharField(max_length=255, verbose_name="Телеграм юзернейм")
    type = models.CharField(max_length=255, choices=COURSES, verbose_name="Направление")

    def __str__(self):
        return self.telegram_username


class Telegram(models.Model):
    text = models.TextField(verbose_name="Текст приветствия",
                            help_text='Внимание! при отправке текста пользователю внутри {} '
                                      'скобок пишется его, не забудьте оставить скобки')
    direction = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name="Направление")
    group_link = models.URLField(max_length=255, verbose_name="Ссылка на группу")

    def __str__(self):
        return self.group_link

