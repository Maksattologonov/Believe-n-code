from django.urls import path, include
from .views import CourseView, SuccessCallback, ResultCallback, PayboxUrl

urlpatterns = [
    path('course/', CourseView.as_view(), name='course'),
    path('api/urls/', PayboxUrl.as_view(), name='urls'),
    path('success_callback', SuccessCallback.as_view(), name='paybox_callback'),
    path('result_callback', ResultCallback.as_view(), name='result_callback'),
    # path('success_callback', PayboxCallback.as_view(), name='success_callback'),

]