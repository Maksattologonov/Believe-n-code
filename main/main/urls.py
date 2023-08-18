
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('payment_app.urls')),
    path('', include('telegram_app.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Администрирование Believe'n'Code"
admin.site.site_url = "https://believencode.io/"
