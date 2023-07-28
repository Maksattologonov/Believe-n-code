from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import (
    TelegramGroup, Mentor, TelegramMessage, ContactUsTelegram, InstallmentTelegram, TelegramBot, TelegramUser)


class MentorAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'direction')


class TelegramGroupAdmin(admin.ModelAdmin):
    list_display = ('direction', 'type', 'group_link')


class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('manager_id', 'id')


class ContactUsTelegramAdmin(admin.ModelAdmin):
    list_display = ('manager_id', 'id')


class InstallmentTelegramAdmin(admin.ModelAdmin):
    list_display = ('manager_id', 'id')


class TelegramBotAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramGroup, TelegramGroupAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(TelegramMessage, TelegramMessageAdmin)
admin.site.register(InstallmentTelegram, InstallmentTelegramAdmin)
admin.site.register(ContactUsTelegram, ContactUsTelegramAdmin)
admin.site.register(TelegramBot, TelegramBotAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)


admin.site.unregister(Group)
