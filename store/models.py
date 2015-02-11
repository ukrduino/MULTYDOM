from django.db import models
from MULTYDOM.settings import SITE_ADDR, STATICFILES_DIRS
from PIL import Image
import os
# for image resizing
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# for validation
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError


class MainClass(models.Model):  # абстрактный класс имеет имя и картинку 160*160
    class Meta:
        abstract = True
        app_label = 'Магазин'

    title = models.CharField(max_length=100, verbose_name='Название', blank=False, unique=True)
    slug = models.CharField(max_length=100, verbose_name='URL')
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
            return '%s/%s' % (SITE_ADDR, self.image.url[39:])
        else:
            return '(none)'

    pic.short_description = 'Изображение'
    pic.allow_tags = True

# функция формирования пути к картинке объекта Product для отображения в админке
    def adminPic(self):
        if self.image:
            return '<img src="%s/%s"/>' % (SITE_ADDR, self.image.url[39:])
        else:
            return '(none)'
    adminPic.short_description = 'Изображение'
    adminPic.allow_tags = True

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
                raise ValidationError(_('Please use an image 160 x 160 pixels'))

            #validate content type
            im_format = img.format
            if not im_format.lower() in ['jpeg', 'png', 'jpg']:
                raise ValidationError(_('Please use a JPEG or PNG image.'))

        else:
            raise ValidationError(_("Couldn't read uploaded image"))

        return image


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

    parentCategory = models.ForeignKey("Category", blank=True, null=True, verbose_name='Входит в группу')

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
    upload_path = '%s/products/' % STATICFILES_DIRS
    productPhoto_original = ProcessedImageField(upload_to=upload_path,
                                                processors=[ResizeToFill(400, 300)],
                                                verbose_name='Фото товара формат (выс4*шир3)')
    productPhoto_medium = models.CharField(max_length=255, blank=True, editable=False)
    productPhoto_thumb = models.CharField(max_length=255, blank=True, editable=False)

    # methods to return paths to the thumbnail, medium, and original images
    def get_thumb(self):
        return '<img src="%s/%s"/>' % (SITE_ADDR, self.productPhoto_thumb[39:])
    get_thumb.allow_tags = True

    def get_medium(self):
        return '%s/%s' % (SITE_ADDR, self.productPhoto_medium[39:])
    get_medium.allow_tags = True

    def get_original(self):

        return '%s/%s' % (SITE_ADDR, self.productPhoto_original.path[39:])
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

        # размеры будущих картинок
        sizes = {'thumbnail': {'height': 100, 'width': 130}, 'medium': {'height': 162, 'width': 216},}
        photopath = str(self.productPhoto_original.path)  # this returns the full system path to the original file
        im = Image.open(photopath)  # open the image using PIL

        # pull a few variables out of that full path
        extension = photopath.rsplit('.', 1)[1]  # the file extension
        filename = photopath.rsplit('/', 1)[1].rsplit('.', 1)[0]  # the file name only (minus path or extension)
        fullpath = photopath.rsplit('/', 1)[0]  # the path only (minus the filename.extension)

        # use the file extension to determine if the image is valid before proceeding
        # if extension not in ['jpg', 'jpeg', 'gif', 'png']:
        #     sys.exit()

        # create medium image
        im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
        medname = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height']) + ".jpg"
        im.save(fullpath + '/' + medname)
        self.productPhoto_medium = self.upload_path + medname

        # create thumbnail
        im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
        thumbname = filename + "_" + str(sizes['thumbnail']['width']) + "x" + str(sizes['thumbnail']['height']) + ".jpg"
        im.save(fullpath + '/' + thumbname)
        self.productPhoto_thumb = self.upload_path + thumbname

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
                raise ValidationError(_('Please use an image with 1.33 aspect ratio and size not less than 400 x 300 '
                                        'pixels, image will be autoresized'))

            #validate content type
            im_format = img.format
            if not im_format.lower() in ['jpeg', 'png', 'jpg']:
                raise ValidationError(_('Please use a JPEG or PNG image.'))

            # #validate file size
            # if len(image) > (1 * 1024 * 1024):
            #     raise ValidationError(_('Image file too large ( maximum 1mb )'))
        else:
            raise ValidationError(_("Couldn't read uploaded image"))

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