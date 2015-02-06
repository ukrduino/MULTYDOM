from django.contrib import admin
from store.models import *  # импортируем модели
# from cart.models import *  # импортируем модели
# "Связывающий" класс  - добавляет в админку одного класса другой класс например в админке класса Product
# будут видны и комментарии к нему (класс Comment)


class ProductAdmin(admin.ModelAdmin):  # класс для перенастройки отображения класса Product в админке
    prepopulated_fields = {'slug': ('title',)}  # из поля product_title транслитом заполняется
                                                                # поле product_slug

    list_display = ['title', 'productDate', 'productDateChange', 'productCurrentPrice', 'productPresence', 'picS']  # возможность просматривать записи
                                                                        # Product в виде таблицы
    list_filter = ['productDate', 'productDateChange', 'productPresence', 'productCategory', 'productManufacturer']  # включение фильтра по датам
    search_fields = ['title']
#    filter_horizontal = ('product_category_MTM',)  # Позволяет управлять  категориями в товаре
                                                   # (добавлять, удалять, менять)


# class OrderAdmin(admin.ModelAdmin):  # класс для перенастройки отображения класса Product в админке
#
#     list_display = ['order_code', 'order_person', 'order_date', 'order_sum', 'order_delivered',
#                     'order_confirmed']  # возможность просматривать записи
#                                         # Order в виде таблицы
#     list_filter = ['order_date', 'order_sum', 'order_delivered', 'order_confirmed']  # включение фильтра по датам
#     search_fields = ['order_code', 'order_person']


class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}  # из поля product_title транслитом заполняется
                                                                # поле product_slug
    list_display = ['title', 'picS']
    search_fields = ['title']


class CategoryAdmin(admin.ModelAdmin):  # класс для перенастройки отображения класса Product в админке
    prepopulated_fields = {'slug': ('title',)}  # из поля product_title транслитом заполняется

    list_display = ['title', 'picS']



# # Register your models here.
admin.site.register(Product, ProductAdmin)  # регистрация класса Product в админке с указанием, что вместо
                                           # него будут настройки описанные в ProductAdmin
# admin.site.register(Order, OrderAdmin)  # регистрация класса Order в админке
admin.site.register(Manufacturer, ManufacturerAdmin)  # регистрация класса Order в админке
admin.site.register(Category, CategoryAdmin)
