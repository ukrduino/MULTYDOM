from django.db import models
# импортируем random  для функции make_upload_path
import random
from MULTYDOM.localSettings import SITE_ADDR

from imagekit import ImageSpec
from imagekit.processors import ResizeToFill


# TODO создание Thumbnail
class Thumbnail(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 60}

# TODO удаление картинки при удалении файла и удаление картинки при удалении картинки или просто удаление картинок непривязанных к объектам
# http://stackoverflow.com/a/16443037/3177550
# http://timonweb.com/cleanup-files-and-images-on-model-delete-in-django
# http://tiku.io/questions/133317/replacing-a-django-image-doesnt-delete-original


# функция Переопределение имени загружаемого файла.  TODO вынести в утилиты
def make_upload_path(instance, filename, prefix=False):
    n1 = random.randint(0, 10000)
    n2 = random.randint(0, 10000)
    n3 = random.randint(0, 10000)
    filename = str(n1)+"_"+str(n2)+"_"+str(n3) + '.jpg'
    return u"%s/%s" % ('static/products', filename)  # и кладет в папку указ. в "settings" в "IMAGE_UPLOAD_DIR"


class MainClass(models.Model):  # абстрактный класс имеет имя и картинку
    class Meta:
        abstract = True
        app_label = 'Магазин'

    title = models.CharField(max_length=100, verbose_name='Название', blank=False, unique=True)
    slug = models.CharField(max_length=100, verbose_name='URL')
    image = models.ImageField(upload_to=make_upload_path, default="", verbose_name='Изображение')

# при обращении к экземпляру класса возвращает его имя - title ( в админке использует __str__, в др местах __unicode__)
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

# TODO Убрать после настроки создания Thumbnail
# функция формирования пути к картинке объекта Product для отображения в админке
    def pic(self):
        if self.image:
            return '<img src="%s/%s"/>' % (SITE_ADDR, self.image.url)
        else:
            return '(none)'
    pic.short_description = 'Изображение'
    pic.allow_tags = True

    # функция формирования пути к картинке объекта Product для отображения в админке
    def picS(self):
        if self.image:
            return '<img src="%s/%s", height="100"/>' % (SITE_ADDR, self.image.url)
        else:
            return '(none)'
    picS.short_description = 'Изображение'
    picS.allow_tags = True


class Manufacturer(MainClass):
    class Meta():
        db_table = 'manufacturer'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    manufacturerText = models.TextField(max_length=1000, verbose_name='Описание производителя')
    manufacturerCountry = models.CharField(max_length=50, verbose_name='Страна производства', blank=False)


class Category(MainClass):
    class Meta():
        db_table = 'category'
        verbose_name = 'Товарная группа'
        verbose_name_plural = 'Товарные группы'

#http://stackoverflow.com/questions/16589069/foreignkey-does-not-allow-null-values
#You must create a migration, where you will specify default value for a new field, since you don't want it to be null.
# If null is not required, simply add null=True and create and run migration.

    parentCategory = models.ForeignKey("Category", blank=True, null=True)

# http://stackoverflow.com/a/6379556/3177550
    MainClass._meta.get_field('image').blank = True


class Product(MainClass):
    class Meta:
        db_table = 'product'  # определяем свое название таблицы в Б.Д.
        verbose_name = 'Товар'  # имя модели в админке в ед ч
        verbose_name_plural = 'Товары'  # имя модели в админке в мн ч

    productText = models.TextField(verbose_name='Описание товара', blank=False)
    productDate = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения', blank=False)
    productDateChange = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    productCurrentPrice = models.IntegerField(verbose_name='Текущая цена', default=0)
    productPresence = models.BooleanField(verbose_name='В наличии', default=True)
    productForOrder = models.BooleanField(verbose_name='Под заказ', default=False)
    productSize = models.CharField(verbose_name='Размер', blank=True, max_length=100)
    productManufacturer = models.ForeignKey(Manufacturer, related_name='products')  # производитель товара
    productCategory = models.ForeignKey(Category, related_name='products')  # производитель товара
