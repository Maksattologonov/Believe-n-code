
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payment_app.urls')),
    path('', include('telegram_app.urls'))
]
