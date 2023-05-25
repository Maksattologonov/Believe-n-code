from django.urls import path, include
from .views import TelegramAPIView

urlpatterns = [
    path('bot/', TelegramAPIView.as_view(), name='bot')
    ]