from django.contrib import admin

from telegram_app.models import Telegram, Mentor


class TelegramAdmin(admin.ModelAdmin):
    pass


class MentorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Telegram, TelegramAdmin)
admin.site.register(Mentor, MentorAdmin)
