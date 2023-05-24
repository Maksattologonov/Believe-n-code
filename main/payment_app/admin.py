from django.contrib import admin
from .models import Course, Tariff, PayboxSuccessPay, TemporaryAccess


class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type')
    search_fields = ('name', 'type')


class TariffAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'new_price')
    search_fields = ('name', 'new_price')


class PayboxSuccessPayAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user_phone', 'name')
    search_fields = ('payment_id', 'name')


class TemporaryAccessAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_number', 'tariff', 'course', 'start_date')


admin.site.register(Course, CourseAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(PayboxSuccessPay, PayboxSuccessPayAdmin)
admin.site.register(TemporaryAccess, TemporaryAccessAdmin)
