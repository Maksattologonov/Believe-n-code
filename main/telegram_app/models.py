from django.db import models


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


