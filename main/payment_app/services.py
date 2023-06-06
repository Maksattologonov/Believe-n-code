import re

from django.db import IntegrityError

from common.exceptions import ObjectNotFoundException, UniqueObjectException, TypeErrorException
from .models import Tariff, Course, PayboxSuccessPay, TemporaryAccess


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

    @classmethod
    def save(cls, order_id, payment_id, amount, currency, description, user_phone, email, signature):
        try:
            obj = Course.objects.get(pk=order_id)
            instance = PayboxSuccessPay(
                order_id=obj.pk,
                payment_id=payment_id,
                signature=signature,
                type=obj.type.name,
                name=obj.name,
                amount=amount if amount else 0,
                currency=currency if currency else " ",
                description=description if description else " ",
                user_phone=user_phone if user_phone else " ",
                email=email if email else " ")
            instance.save()
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


class TemporaryAccessService:
    model = TemporaryAccess

    @classmethod
    def get(cls, **filters):
        try:
            obj = cls.model.objects.filter(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Object not found')

    @classmethod
    def create_access(cls, name: str, telegram_number: str, tariff: str, course: str) -> TemporaryAccess:
        try:
            tariff_instance = Tariff.objects.get(name=tariff)
            course_instance = Course.objects.get(name=course, type=tariff_instance.id)
            if tariff_instance and course_instance:
                new_event = cls.model.objects.create(name=name, telegram_number=telegram_number,
                                                     tariff=tariff_instance, course=course_instance)
                return course_instance.temporary_lms_url
            else:
                raise TypeErrorException("Bad credentials")
        except Tariff.DoesNotExist:
            raise ObjectNotFoundException('Tariff not found')
        except Course.DoesNotExist:
            raise ObjectNotFoundException('Course not found')
        except IntegrityError:
            raise UniqueObjectException('Unique error')
