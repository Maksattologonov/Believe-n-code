from django.contrib import admin
from django.contrib.auth.models import User, Group
from telegram_app.models import TelegramGroup, Mentor, TelegramMessage, ContactUsTelegram, InstallmentTelegram


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


admin.site.register(TelegramGroup, TelegramGroupAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(TelegramMessage, TelegramMessageAdmin)
admin.site.register(InstallmentTelegram, InstallmentTelegramAdmin)
admin.site.register(ContactUsTelegram, ContactUsTelegramAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
