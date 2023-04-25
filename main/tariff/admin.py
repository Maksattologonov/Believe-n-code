from django.contrib import admin

from .models import Tariff, Telegram, Mentor


class TariffAdmin(admin.ModelAdmin):
    pass


class TelegramAdmin(admin.ModelAdmin):
    pass


class MentorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tariff, TariffAdmin)

admin.site.register(Telegram, TelegramAdmin)
admin.site.register(Mentor, MentorAdmin)
