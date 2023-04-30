from django.contrib import admin

from payment_app.models import Tariff, PayboxUrl


class TariffAdmin(admin.ModelAdmin):
    pass


class UrlsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tariff, TariffAdmin)
admin.site.register(PayboxUrl, UrlsAdmin)
