from django.urls import path, include
from .views import PayboxView

urlpatterns = [
    path('tariff/', PayboxView.as_view(), name='pay'),
    # path('payment/', payment, name='payment'),
]