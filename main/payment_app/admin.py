from django.contrib import admin
from .models import Course, Tariff, PayboxSuccessPay, TemporaryAccess, PromoCode, Webinar


class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'type')
    search_fields = ('pk', 'name', 'type')


class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'price')


class PayboxSuccessPayAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user_phone', 'name')
    search_fields = ('payment_id', 'name')


class TemporaryAccessAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_number', 'tariff', 'course', 'start_date')


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of',)


class WebinarAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(PayboxSuccessPay, PayboxSuccessPayAdmin)
admin.site.register(TemporaryAccess, TemporaryAccessAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Webinar, WebinarAdmin)
