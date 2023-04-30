from bot import TelegramBot


class TelegramBotService:
    model = TelegramBot

    @classmethod
    def save(cls, username: str, name: str, user_chat_id: int):
        try:
            obj = cls.model(username=username, name=name, user_chat_id=user_chat_id)
            obj.save()
        except Exception as ex:
            return ex
