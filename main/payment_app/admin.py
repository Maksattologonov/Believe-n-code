from django.contrib import admin

from .models import Course, Tariff


class CourseAdmin(admin.ModelAdmin):
    pass


class TariffAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Tariff, TariffAdmin)
