from django.contrib import admin

from telegram_app.models import Telegram, Mentor, TelegramUser


class TelegramAdmin(admin.ModelAdmin):
    pass


class MentorAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Telegram, TelegramAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
