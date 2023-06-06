from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_app.serializers import TelegramBotSerializer
from telegram_app.services import TelegramBotService


class TelegramAPIView(APIView):
    def get(self, *args, **kwargs):
        queryset = TelegramBotService.get()
        if queryset is not None:
            serializer = TelegramBotSerializer(queryset, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
