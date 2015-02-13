from django.contrib import admin
from store.models import *


# класс для перенастройки отображения класса Product в админке
class ProductAdmin(admin.ModelAdmin):
    # из поля product_title транслитом заполняется поле product_slug
    prepopulated_fields = {'productSlug': ('productTitle',)}
    # возможность просматривать записи Product в виде таблицы
    list_display = ['productTitle', 'productDate', 'productDateChange',
                    'productCurrentPrice', 'productPresence', 'get_thumb']
    # включение фильтра по датам
    list_filter = ['productDate', 'productDateChange', 'productPresence', 'productCategory', 'productManufacturer']

    search_fields = ['productTitle']
#    filter_horizontal = ('product_category_MTM',)  # Позволяет управлять  категориями в товаре
                                                   # (добавлять, удалять, менять)


class ManufacturerAdmin(admin.ModelAdmin):
    # из поля product_title транслитом заполняется поле product_slug
    prepopulated_fields = {'slug': ('title',)}

    list_display = ['title', 'admin_pic']
    search_fields = ['title']


# класс для перенастройки отображения класса Product в админке
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    list_display = ['title', 'admin_pic']

# # Register your models here.
# регистрация класса Product в админке с указанием, что вместо него будут настройки описанные в ProductAdmin
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)