from django.contrib import admin
from store.models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = 'Изображение'
    verbose_name_plural = 'Изображения товара для страницы товара'


# класс для перенастройки отображения класса Product в админке
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    # из поля product_title транслитом заполняется поле product_slug
    prepopulated_fields = {'product_slug': ('product_title',)}
    # возможность просматривать записи Product в виде таблицы
    list_display = ['product_title', 'product_add_date', 'product_change_date',
                    'product_current_price', 'product_present']
    # включение фильтра по датам
    list_filter = ['product_add_date', 'product_change_date', 'product_present', 'category', 'manufacturer']

    search_fields = ['product_title']
#    filter_horizontal = ('product_category_MTM',)  # Позволяет управлять  категориями в товаре
                                                   # (добавлять, удалять, менять)


class ManufacturerLogoInline(admin.TabularInline):
    model = ManufacturerLogo
    extra = 1
    verbose_name_plural = 'Логотип производителя'


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1
    verbose_name_plural = 'Картинка категории'


class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'manufacturer_slug': ('manufacturer_title',)}
    list_display = ['manufacturer_title']
    search_fields = ['manufacturer_title']
    inlines = [ManufacturerLogoInline, ]


# класс для перенастройки отображения класса Product в админке
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_title',)}
    list_display = ['category_title']
    inlines = [CategoryImageInline, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)


