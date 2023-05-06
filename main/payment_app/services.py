from common.exceptions import ObjectNotFoundException
from .models import PayboxUrl


class PayboxUrlsService:
    model = PayboxUrl

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Url not found')
