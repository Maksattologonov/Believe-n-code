from common.exceptions import ObjectNotFoundException
from .models import Tariff, PayboxSuccessPayment, Course


class PayboxUrlsService:
    model = Tariff

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.filter(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Tariff not found')


class PayboxCallbackService:
    model = PayboxSuccessPayment

    @classmethod
    def save(cls, **filters):
        return


class CourseService:
    models = Course

    @classmethod
    def get(cls, **filters):
        try:

            return cls.models.objects.filter(**filters)
        except cls.models.DoesNotExist:
            raise ObjectNotFoundException('Courses not found')
