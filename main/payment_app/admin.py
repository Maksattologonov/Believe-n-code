from django.contrib import admin

from .models import Course, Tariff, PayboxSuccessPay, TemporaryAccess


class CourseAdmin(admin.ModelAdmin):
    pass


class TariffAdmin(admin.ModelAdmin):
    pass


class PayboxSuccessPayAdmin(admin.ModelAdmin):
    pass


class TemporaryAccessAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(PayboxSuccessPay, PayboxSuccessPayAdmin)
admin.site.register(TemporaryAccess, TemporaryAccessAdmin)
