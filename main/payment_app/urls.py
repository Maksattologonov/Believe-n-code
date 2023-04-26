from django.urls import path, include
from .views import DirectionView, PaymentView

urlpatterns = [
    path('directions/', DirectionView.as_view(), name='pay'),
    path('payment/', PaymentView.as_view(), name='payment'),
]