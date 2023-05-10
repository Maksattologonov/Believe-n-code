import re

from common.exceptions import ObjectNotFoundException
from .models import Tariff, Course, PayboxSuccessPay


class PayboxService:
    model = Tariff

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.filter(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Tariff not found')


class PayboxCallbackService:
    model = PayboxSuccessPay

    @staticmethod
    def save(payment_id, amount, currency, description, user_phone, email, signature):
        model = PayboxSuccessPay()
        model.payment_id = payment_id
        model.amount = amount if amount else 0
        model.currency = currency if currency else " "
        model.description = description if description else " "
        model.user_phone = user_phone if user_phone else " "
        model.email = email if email else " "
        model.signature = signature

        try:
            model.save()
        except Exception as ex:
            print(f"Ошибка сохранения: {str(ex)}")

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Payment not found')

    @staticmethod
    def process_text(text):
        cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)
        lowercase_text = cleaned_text.lower()

        return lowercase_text


class CourseService:
    models = Course

    @classmethod
    def get(cls, **filters):
        try:

            return cls.models.objects.filter(**filters)
        except cls.models.DoesNotExist:
            raise ObjectNotFoundException('Courses not found')
