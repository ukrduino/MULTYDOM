from django.db import models
from MULTYDOM.localSettings import SITE_ADDR
from PIL import Image
import sys, os
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class MainClass(models.Model):  # абстрактный класс имеет имя и картинку
    class Meta:
        abstract = True
        app_label = 'Магазин'

    title = models.CharField(max_length=100, verbose_name='Название', blank=False, unique=True)
    slug = models.CharField(max_length=100, verbose_name='URL')
    upload_path ='static/other'
    image = ProcessedImageField(upload_to=upload_path,
                                processors=[ResizeToFill(160, 160)],
                                format='JPEG')

# при обращении к экземпляру класса возвращает его имя - title ( в админке использует __str__, в др местах __unicode__)
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

# функция формирования пути к картинке объекта Product для отображения в админке
    def pic(self):
        if self.image:
            return '<img src="%s/%s"/>' % (SITE_ADDR, self.image.url)
        else:
            return '(none)'
    pic.short_description = 'Изображение'
    pic.allow_tags = True

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            old = self.__class__._default_manager.get(pk=self.pk)
            if old.image.name and (not self.image._committed or not self.image.name):
                old.image.delete(save=False)
        super().save(*args, **kwargs)


class Manufacturer(MainClass):
    class Meta():
        db_table = 'manufacturer'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    manufacturerText = models.TextField(max_length=1000, verbose_name='Описание производителя')
    manufacturerCountry = models.CharField(max_length=50, verbose_name='Страна производства', blank=False)


# MainClass._meta.get_field('image').blank = True


class Category(MainClass):
    class Meta():
        db_table = 'category'
        verbose_name = 'Товарная группа'
        verbose_name_plural = 'Товарные группы'

# http://stackoverflow.com/questions/16589069/foreignkey-does-not-allow-null-values
# You must create a migration, where you will specify default value for a new field, since you don't want it to be null.
# If null is not required, simply add null=True and create and run migration.

    parentCategory = models.ForeignKey("Category", blank=True, null=True)

# http://stackoverflow.com/a/6379556/3177550
# MainClass._meta.get_field('image').blank = True


class Product(models.Model):
    class Meta:
        db_table = 'product'  # определяем свое название таблицы в Б.Д.
        verbose_name = 'Товар'  # имя модели в админке в ед ч
        verbose_name_plural = 'Товары'  # имя модели в админке в мн ч

    productTitle = models.CharField(max_length=100, verbose_name='Название товара', blank=False, unique=True)
    productSlug = models.CharField(max_length=100, verbose_name='URL')
    productText = models.TextField(verbose_name='Описание товара', blank=False, max_length=500)
    productDate = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения', blank=False)
    productDateChange = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    productCurrentPrice = models.IntegerField(verbose_name='Текущая цена', default=0)
    productPresence = models.BooleanField(verbose_name='В наличии', default=True)
    productForOrder = models.BooleanField(verbose_name='Под заказ', default=False)
    productSize = models.CharField(verbose_name='Размер', blank=True, max_length=100)
    productManufacturer = models.ForeignKey(Manufacturer)  # производитель товара
    productCategory = models.ForeignKey(Category)  # производитель товара

# http://www.mechanicalgirl.com/view/image-resizing-file-uploads-doing-it-easy-way/
    filepath = 'static/products/'
    productPhoto_original = ProcessedImageField(upload_to=filepath,
                                                processors=[ResizeToFill(400, 300)],

                                                verbose_name='Фото товара формат (выс4*шир3)')
    productPhoto_medium = models.CharField(max_length=255, blank=True, editable=False)
    productPhoto_thumb = models.CharField(max_length=255, blank=True, editable=False)

    # methods to return paths to the thumbnail, medium, and original images
    def get_thumb(self):
        return '<img src="%s/%s"/>' % (SITE_ADDR, self.productPhoto_thumb)
    get_thumb.allow_tags = True

    def get_medium(self):
        return '%s/%s' % (SITE_ADDR, self.productPhoto_medium)
    get_medium.allow_tags = True

    def get_original(self):
        return '%s/%s' % (SITE_ADDR, self.productPhoto_original)
    get_original.allow_tags = True

    # And all the image resizing magic happens here, where I'm overriding the model's save() method.
    def save(self, *args, **kwargs):

# http://tiku.io/questions/133317/replacing-a-django-image-doesnt-delete-original
# В случае замены картинки удаляет старые файлы картинок привязанные к товару.
        if self.pk:

            old = self.__class__._default_manager.get(pk=self.pk) # товар до сохранения

            if old.productPhoto_original.name and (not self.productPhoto_original._committed or not self.productPhoto_original.name):
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
        Product.clean(self)

        # размеры будущих картинок
        sizes = {'thumbnail': {'height': 100, 'width': 130}, 'medium': {'height': 162, 'width': 216},}
        photopath = str(self.productPhoto_original.path)  # this returns the full system path to the original file
        im = Image.open(photopath)  # open the image using PIL

        # pull a few variables out of that full path
        extension = photopath.rsplit('.', 1)[1]  # the file extension
        filename = photopath.rsplit('/', 1)[1].rsplit('.', 1)[0]  # the file name only (minus path or extension)
        fullpath = photopath.rsplit('/', 1)[0]  # the path only (minus the filename.extension)

        # use the file extension to determine if the image is valid before proceeding
        if extension not in ['jpg', 'jpeg', 'gif', 'png']:
            sys.exit()

        # create medium image
        im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
        medname = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height']) + ".jpg"
        im.save(fullpath + '/' + medname)
        self.productPhoto_medium = self.filepath + medname

        # create thumbnail
        im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
        thumbname = filename + "_" + str(sizes['thumbnail']['width']) + "x" + str(sizes['thumbnail']['height']) + ".jpg"
        im.save(fullpath + '/' + thumbname)
        self.productPhoto_thumb = self.filepath + thumbname

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.productTitle

    def __unicode__(self):
        return self.productTitle




    def clean(self):
        print("clean_productPhoto_original")
        image = self.productPhoto_original

        if image:
            img = Image.open(image)
            w, h = img.size

            #validate dimensions
            max_width = max_height = 10
            if w > max_width or h > max_height:
                raise ValidationError(_('Please use an image that is smaller or equal to '
                      '%s x %s pixels.' % (max_width, max_height)))

            # #validate content type
            # main, sub = image.content_type.split('/')
            # if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
            #     raise ValidationError(_('Please use a JPEG or PNG image.'))
            #
            # #validate file size
            # if len(image) > (1 * 1024 * 1024):
            #     raise ValidationError(_('Image file too large ( maximum 1mb )'))
        else:
            raise ValidationError(_("Couldn't read uploaded image"))
        return image

