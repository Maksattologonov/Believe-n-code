from django.contrib import admin
from django.contrib.auth.models import User, Group


admin.site.unregister(User)

admin.site.unregister(Group)


from telegram_app.models import TelegramGroup, Mentor, TelegramMessage, ContactUsTelegram, InstallmentTelegram


class MentorAdmin(admin.ModelAdmin):
    pass


class TelegramGroupAdmin(admin.ModelAdmin):
    pass


class TelegramMessageAdmin(admin.ModelAdmin):
    pass


class ContactUsTelegramAdmin(admin.ModelAdmin):
    pass


class InstallmentTelegramAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramGroup, TelegramGroupAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(TelegramMessage, TelegramMessageAdmin)
admin.site.register(InstallmentTelegram, InstallmentTelegramAdmin)
