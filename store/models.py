from django.db import models
#TODO - избавиться от TRIM_PATH переделав алгоритм загрузки фото
from MULTYDOM.settings import SITE_ADDR, STATICFILES_DIRS, TRIM_PATH, TRIM_PATH_PROD
from PIL import Image
import os
import sys
# for image resizing
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# for validation
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
# from ckeditor.fields import RichTextField


validation_message1 = 'Используйте квадратное изображение размером не менее 160 x 160 pixels'
validation_message2 = 'Используйте изображение формата  JPEG или PNG.'
validation_message3 = 'Загруженный файл не читается'
validation_message4 = 'Используйте изображение с соотношением сторон Ширина/Высота = 1.33 и размером не менее 400 x 300,' \
                      ' оно будет автоматически уменьшено'


# абстрактный класс имеет имя и картинку 160*160
class MainClass(models.Model):
    class Meta:
        abstract = True
        app_label = 'Магазин'

    title = models.CharField(max_length=100, verbose_name='Название', blank=False, unique=True)
    slug = models.CharField(max_length=100, verbose_name='URL')
    #TODO - сделать переименование файлов при загрузке с использованием slug
    upload_path = '%s/other' % STATICFILES_DIRS
    image = ProcessedImageField(upload_to=upload_path,
                                processors=[ResizeToFill(160, 160)],
                                format='JPEG')

# при обращении к экземпляру класса возвращает его имя - title ( в админке использует __str__, в др местах __unicode__)
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def pic(self):
        if self.image:
            return '%s/%s' % (SITE_ADDR, self.image.url[TRIM_PATH:])
        else:
            return '(none)'
    pic.short_description = 'Изображение'
    pic.allow_tags = True

# функция формирования пути к картинке объекта для отображения в админке

    def admin_pic(self):
        if self.image:
            return '<img src="%s/%s"/>' % (SITE_ADDR, self.image.url[TRIM_PATH:])
        else:
            return '(none)'
    admin_pic.short_description = 'Изображение'
    admin_pic.allow_tags = True

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old = self.__class__._default_manager.get(pk=self.pk)
            if old.image.name and (not self.image._committed or not self.image.name):
                old.image.delete(save=False)
        super().save(*args, **kwargs)

    def clean(self):
        image = self.image

        if image:
            #validate dimensions
            img = Image.open(image)
            w, h = img.size
            if w != h:
                raise ValidationError(_(validation_message1))

            #validate content type
            im_format = img.format
            if not im_format.lower() in ['jpeg', 'png', 'jpg']:
                raise ValidationError(_(validation_message2))

        else:
            raise ValidationError(_(validation_message3))

        return image


class Manufacturer(MainClass):
    class Meta():
        db_table = 'manufacturer'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    manufacturerText = models.TextField(max_length=1000, verbose_name='Описание производителя', blank=True)
    manufacturerCountry = models.CharField(max_length=50, verbose_name='Страна производства', blank=True)


class Category(MainClass, MPTTModel):
    class Meta():
        db_table = 'category'
        verbose_name = 'Товарная группа'
        verbose_name_plural = 'Товарные группы'

    class MPTTMeta:
        order_insertion_by = ['title']
# http://stackoverflow.com/questions/16589069/foreignkey-does-not-allow-null-values
# You must create a migration, where you will specify default value for a new field, since you don't want it to be null.
# If null is not required, simply add null=True and create and run migration.

    # parentCategory = models.ForeignKey("Category", blank=True, null=True, verbose_name='Входит в группу')

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                                    verbose_name='Входит в группу')

# http://stackoverflow.com/a/6379556/3177550
# MainClass._meta.get_field('image').blank = True


#TODO - а как начет нескольких картинок товара???
class Product(models.Model):
    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    productTitle = models.CharField(max_length=100, verbose_name='Название товара', blank=False, unique=True)
    productSlug = models.CharField(max_length=100, verbose_name='URL')
    # productText = RichTextField(verbose_name='Описание товара', blank=False)
    productDate = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения', blank=False)
    productDateChange = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    productStartPrice = models.IntegerField(verbose_name='Начальная цена', default=0)
    productStartPriceInDollars = models.BooleanField(verbose_name='Цена в долларах', default=False)
    productCurrentPrice = models.IntegerField(verbose_name='Текущая цена', default=0)
    productPresence = models.BooleanField(verbose_name='В наличии', default=True)
    productForOrder = models.BooleanField(verbose_name='Под заказ', default=False)
    productSize = models.CharField(verbose_name='Размер(без слова "размер")', blank=True, max_length=100)
    productManufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель')
    productCategory = models.ForeignKey(Category, verbose_name='Категория товара')

# http://www.mechanicalgirl.com/view/image-resizing-file-uploads-doing-it-easy-way/
    upload_path = '%s/products/' % STATICFILES_DIRS
    productPhoto_original = ProcessedImageField(upload_to=upload_path,
                                                processors=[ResizeToFill(400, 300)],
                                                verbose_name='Фото товара формат (выс4*шир3)')
    productPhoto_medium = models.CharField(max_length=255, blank=True, editable=False)
    productPhoto_thumb = models.CharField(max_length=255, blank=True, editable=False)

    # methods to return paths to the thumbnail, medium, and original images
    if sys.platform.startswith('win32'):
        def get_thumb(self):
            return '<img src="%s/%s"/>' % (SITE_ADDR, self.productPhoto_thumb[TRIM_PATH_PROD:])
        get_thumb.allow_tags = True

        def get_thumb_cart(self):
            return '%s/%s' % (SITE_ADDR, self.productPhoto_thumb[TRIM_PATH_PROD:])
        get_thumb.allow_tags = True

        def get_medium(self):
            return '%s/%s' % (SITE_ADDR, self.productPhoto_medium[TRIM_PATH_PROD:])
        get_medium.allow_tags = True

        def get_original(self):

            return '%s/%s' % (SITE_ADDR, self.productPhoto_original.path[TRIM_PATH_PROD:])
        get_original.allow_tags = True

    else:
        def get_thumb(self):
            return '<img src="%s/%s"/>' % (SITE_ADDR, self.productPhoto_thumb[TRIM_PATH:])
        get_thumb.allow_tags = True

        def get_thumb_cart(self):
            return '%s/%s' % (SITE_ADDR, self.productPhoto_thumb[TRIM_PATH:])
        get_thumb.allow_tags = True

        def get_medium(self):
            return '%s/%s' % (SITE_ADDR, self.productPhoto_medium[TRIM_PATH:])
        get_medium.allow_tags = True

        def get_original(self):

            return '%s/%s' % (SITE_ADDR, self.productPhoto_original.path[TRIM_PATH:])
        get_original.allow_tags = True

    def delete(self, *args, **kwargs):
        self.productPhoto_original.delete(save=False)
        os.remove(self.productPhoto_medium)
        os.remove(self.productPhoto_thumb)

        super().delete(*args, **kwargs)

    # And all the image resizing magic happens here, where I'm overriding the model's save() method.
    def save(self, *args, **kwargs):

# http://tiku.io/questions/133317/replacing-a-django-image-doesnt-delete-original
# В случае замены картинки удаляет старые файлы картинок привязанные к товару.
        if self.pk:
            # товар до сохранения
            old = self.__class__._default_manager.get(pk=self.pk)

            if old.productPhoto_original.name and (not self.productPhoto_original._committed
                                                   or not self.productPhoto_original.name):
                # удаляем основное фото
                old.productPhoto_original.delete(save=False)
                # Удаляем medium
                try:
                    os.remove(old.productPhoto_medium)
                except:
                    pass
                # Удаляем thumb
                try:
                    os.remove(old.productPhoto_thumb)
                except:
                    pass
        # clean_productPhoto_original(self)
        super(Product, self).save()

        # размеры будущих картинок
        sizes = {'thumbnail': {'height': 100, 'width': 130}, 'medium': {'height': 162, 'width': 216},}
        photo_path = str(self.productPhoto_original.path)  # this returns the full system path to the original file
        im = Image.open(photo_path)  # open the image using PIL

        print(sys.platform)
        slash_symb = "/"
        if sys.platform.startswith('win32'):
            # win32-specific code here...
            slash_symb = "\\"
        # pull a few variables out of that full path
        # extension = photo_path.rsplit('.', 1)[1]  # the file extension
        filename = photo_path.rsplit(slash_symb, 1)[1].rsplit('.', 1)[0]  # the file name only (minus path or extension)
        full_path = photo_path.rsplit(slash_symb, 1)[0]  # the path only (minus the filename.extension)

        # create medium image
        im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
        med_name = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height']) + ".jpg"
        im.save(full_path + slash_symb + med_name)
        self.productPhoto_medium = self.upload_path + med_name

        # create thumbnail
        im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
        thumb_name = filename + "_" + str(sizes['thumbnail']['width']) \
                              + "x" + str(sizes['thumbnail']['height']) + ".jpg"
        im.save(full_path + slash_symb + thumb_name)
        self.productPhoto_thumb = self.upload_path + thumb_name

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.productTitle

    def __unicode__(self):
        return self.productTitle

    def clean(self):
        image = self.productPhoto_original
        print(image)

        if image:
            #validate dimensions
            img = Image.open(image)
            w, h = img.size
            img_asp_ratio = float(format(w/h, '.2f'))
            my_asp_ratio = float(format(400/300, '.2f'))
            if img_asp_ratio != my_asp_ratio and (w < 400 or h < 300):
                raise ValidationError(_(validation_message4))

            #validate content type
            im_format = img.format
            if not im_format.lower() in ['jpeg', 'png', 'jpg']:
                raise ValidationError(_(validation_message2))

            # #validate file size
            # if len(image) > (1 * 1024 * 1024):
            #     raise ValidationError(_('Image file too large ( maximum 1mb )'))
        else:
            raise ValidationError(_(validation_message3))

        return image

# Programmatically saving image to Django ImageField
# http://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield

# Django: add image in an ImageField from image url
# http://stackoverflow.com/questions/1393202/django-add-image-in-an-imagefield-from-image-url

# django imagekit: set ProcessedImageField from image url
# http://stackoverflow.com/questions/19386866/django-imagekit-set-processedimagefield-from-image-url
# http://www.wenda.io/questions/5011020/django-imagekit-set-processedimagefield-from-image-url.html

# Generates thumbnails after image is uploaded into memory
# http://djangothumbnails.com/

# How to resize the new uploaded images using PIL before saving?
# http://stackoverflow.com/questions/7970637/how-to-resize-the-new-uploaded-images-using-pil-before-saving
# https://github.com/un1t/django-resized