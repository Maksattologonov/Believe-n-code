from django.contrib import admin

from telegram_app.models import TelegramGroup, Mentor


class MentorAdmin(admin.ModelAdmin):
    pass


class TelegramGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramGroup, TelegramGroupAdmin)
admin.site.register(Mentor, MentorAdmin)