from django.urls import path, include
from .views import CourseView, SuccessCallback, ResultCallback, PayboxUrl

urlpatterns = [
    path('course/', CourseView.as_view(), name='course'),
    path('tariff/', PayboxUrl.as_view(), name='tariff'),
    path('success_callback', SuccessCallback.as_view(), name='paybox_callback'),
    path('result_callback', ResultCallback.as_view(), name='result_callback'),
]