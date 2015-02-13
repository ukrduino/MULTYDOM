from django.contrib import admin
from cart.models import *


# класс для перенастройки отображения класса Product в админке
class OrderAdmin(admin.ModelAdmin):
    # возможность просматривать записи Order в виде таблицы
    list_display = ['order_code', 'order_person', 'order_date', 'order_sum', 'order_delivered',
                    'order_confirmed']
    # включение фильтра по датам
    list_filter = ['order_date', 'order_sum', 'order_delivered', 'order_confirmed']
    search_fields = ['order_code', 'order_person']

# регистрация класса Order в админке
admin.site.register(Order, OrderAdmin)