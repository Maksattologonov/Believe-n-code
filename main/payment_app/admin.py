from django.contrib import admin

from .models import Course, Tariff, PayboxSuccessPay


class CourseAdmin(admin.ModelAdmin):
    pass


class TariffAdmin(admin.ModelAdmin):
    pass


class PayboxSuccessPayAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(PayboxSuccessPay, PayboxSuccessPayAdmin)
