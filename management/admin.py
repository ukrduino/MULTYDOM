from django.contrib import admin
from management.models import Dollar, PriceIndex


# класс для перенастройки отображения класса Dollar в админке
class DollarAdmin(admin.ModelAdmin):
    # возможность просматривать записи Dollar в виде таблицы
    list_display = ["dollar_date", "dollar_to_hrn", "dollar_active"]


# регистрация класса Dollar в админке
admin.site.register(Dollar, DollarAdmin)

# класс для перенастройки отображения класса PriceIndex в админке
class PriceIndexAdmin(admin.ModelAdmin):
    # возможность просматривать записи PriceIndex в виде таблицы
    list_display = ["priceIndex_date", "priceIndexValue", "priceIndex_active"]


# регистрация класса PriceIndex в админке
admin.site.register(PriceIndex, PriceIndexAdmin)