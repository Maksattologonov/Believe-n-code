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

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'


class Telegram(models.Model):
    chat_welcome_text = models.TextField(verbose_name="Текст приветствия в личных сообщениях",
                                         help_text='Внимание! при отправке текста пользователю внутри  '
                                                   'скобок пишется его, не забудьте оставить скобки')
    direction = models.ForeignKey(Mentor, on_delete=models.CASCADE, verbose_name="Направление")
    installment_program = models.TextField(verbose_name="Текст приветствия для программы рассрочки")
    manager_telegram_id = models.IntegerField(verbose_name="ID группы с менеджером телеграм")

    def __str__(self):
        return self.installment_program

    class Meta:
        verbose_name = 'Текст для Телеграма'
        verbose_name_plural = 'Тексты для Телеграма'


class TelegramGroup(models.Model):
    name = models.CharField(verbose_name="Название группы", max_length=255)
    group_welcome_text = models.TextField(verbose_name="Текст приветствия в группе",
                                          help_text='Внимание! при отправке текста пользователю внутри {} '
                                                    'скобок пишется его, не забудьте оставить скобки')
    group_link = models.URLField(max_length=1000, verbose_name="ID группы телеграма")

    class Meta:
        verbose_name = "Группа телеграм"
        verbose_name_plural = "Группы телеграм"

    def __str__(self):
        return self.name


class TelegramUser(models.Model):
    username = models.CharField(max_length=100, verbose_name="Юзернейм")
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    user_chat_id = models.IntegerField(verbose_name="ID переписки")

    class Meta:
        verbose_name = 'Пользователь Телеграма'
        verbose_name_plural = 'Пользователи Телеграма'

    def __str__(self):
        return self.name
