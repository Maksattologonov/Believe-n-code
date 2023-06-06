from common.exceptions import ObjectNotFoundException
from telegram_app.models import TelegramBot


class TelegramBotService:
    model = TelegramBot

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Telegram account not found')
