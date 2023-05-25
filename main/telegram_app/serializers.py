from rest_framework import serializers

from telegram_app.models import TelegramBot


class TelegramBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = ("bot_link",)
