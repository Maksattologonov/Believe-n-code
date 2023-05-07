from django.urls import path, include
from .views import DirectionView, paybox_callback, PayboxUrl

urlpatterns = [
    path('directions/', DirectionView.as_view(), name='pay'),
    path('paybox_callback', paybox_callback, name='paybox_callback'),
    path('api/urls/', PayboxUrl.as_view(), name='urls'),

]