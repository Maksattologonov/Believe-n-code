from django.urls import path, include
from .views import CourseView, SuccessCallback, ResultCallback, PayboxUrl, TemporaryAccessAPIView, WebinarAPIView

urlpatterns = [
    path('course/', CourseView.as_view(), name='course'),
    path('tariff/', PayboxUrl.as_view(), name='tariff'),
    path('success_callback', SuccessCallback.as_view(), name='success_callback'),
    path('result_callback', ResultCallback.as_view(), name='result_callback'),
    path('access_create', TemporaryAccessAPIView.as_view(), name='access_create'),
    path('webinar', WebinarAPIView.as_view(), name='webinar'),
]
