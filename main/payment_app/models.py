import datetime

from django.db import models
from django.utils import timezone


class Tariff(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название тарифа")
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    type = models.ForeignKey(Tariff, verbose_name="Тариф курса", on_delete=models.CASCADE)
    lms_url = models.URLField(verbose_name="Ссылка на курс", max_length=1500)
    # temporary_lms_url = models.URLField(verbose_name="Временная ссылка на курс", max_length=1500)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f'{self.name}, {self.type}'


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
    telegram_number = models.CharField(max_length=20, verbose_name='Телеграм номер', unique=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата начала доступа')

    class Meta:
        verbose_name = 'Временный доступ'
        verbose_name_plural = 'Временные доступы'

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    name = models.CharField(max_length=20, help_text='Максимум 20 символов', verbose_name='Промокод', unique=True)
    date_of = models.DateField(verbose_name='Дата действия промокода', default=timezone.now)

    class Meta:
        verbose_name = 'Паромокод'
        verbose_name_plural = 'Паромокоды'

    def __str__(self):
        return self.name


class Webinar(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема вебинара')
    date_time = models.DateTimeField(default=timezone.now, verbose_name='Дата начала',
                                     help_text='Вводите время по часовому поясу Бишкека')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, verbose_name='Промокод',
                                   help_text='Только на латыни')
    group_url = models.URLField(max_length=255, verbose_name="Ссылка на группу")
    welcome_text = models.TextField(verbose_name='Текст приветствия',
                                    help_text='Обязательно оставьте {} для вставки имени пользователя, '
                                              'наример: Привет {}!',
                                    default='{} как здорово что ты с нами!')
    choose_text = models.TextField(verbose_name='Текст после выбора города',
                                   help_text='Обязательно оставьте {} для вставки имени пользователя, '
                                             'наример: Привет {}!',
                                   default='ваш ответ записан. Вебинар начнется в {}')
    text = models.TextField(verbose_name='Текст напоминания')
    image = models.ImageField(upload_to='media/webinar', verbose_name='Изображение для рассылки',
                              help_text='формат обязательно jpeg, png, webp')

    class Meta:
        verbose_name = 'Вебинар'
        verbose_name_plural = 'Вебинары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and Webinar.objects.exists():
            return Webinar.objects.update_or_create(*args, **kwargs)
        return super(Webinar, self).save(*args, **kwargs)
