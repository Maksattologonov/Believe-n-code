from django.contrib import admin

from payment_app.models import Tariff


class TariffAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tariff, TariffAdmin)
