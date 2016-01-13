from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from MULTYDOM.local_settings_multydom import SITE_ADDR
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from PIL import Image
from ckeditor.fields import RichTextField


size_validation_message_160_160 = 'Используйте квадратное изображение размером не менее 160 x 160 pixels'
format_validation_message_jpg_png = 'Используйте изображение формата  JPEG или PNG.'
invalid_image_file_validation_message = 'Загруженный файл не читается'
size_validation_message_w400_h300 = 'Используйте изображение с соотношением сторон Ширина/Высота = 1.33 и размером ' \
                                    'не менее 400 x 300, оно будет автоматически уменьшено'
size_validation_message_w130_h100 = 'Используйте изображение с соотношением сторон Ширина/Высота = 1.33 и размером ' \
                                    'не менее 130 x 100, оно будет автоматически уменьшено'


class CategoryManufacturerImage(models.Model):
    """
    Абстрактный класс изображения для категории и производителя
    """
    class Meta:
        abstract = True

    image = ProcessedImageField(upload_to='other/%Y/%m/%d',
                                processors=[ResizeToFill(160, 160)],
                                format='JPEG')

    # TODO Проверить валидацию файла при загрузке

    def delete(self, *args, **kwargs):
        """
        Метод для удаления файла с диска при удалении экземпляра класса рисунка из БД,
        работает если производить удаление именно объекта рисунка из админки,
        а не объекта производителя или категории и как следствие -> каскадно
        объекта рисунка связанного с ним.
        """
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def clean(self):
        """
        Метод для валидации изображения перед сохранением (Используется Pillow).
        """
        image = self.image

        if image:
            # валидация размеров
            img = Image.open(image)
            w, h = img.size
            if w != h:
                raise ValidationError(size_validation_message_160_160)

        else:
            raise ValidationError(invalid_image_file_validation_message)

        return image

    def save(self, *args, **kwargs):
        """
        Метод для удаления файла с диска при замене старого изображения(файла)
        новым в объекте рисунка без создания нового объекта рисунка.
        Пустые папки при этом не удаляются.
        """

        if self.pk:
            old = self.__class__._default_manager.get(pk=self.pk)
            if old.image.name and (not self.image._committed or not self.image.name):
                old.image.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Формирует тэг для отображения файла в админке
        """
        if self.image:
            return mark_safe('<img src="%s%s"/>' % (SITE_ADDR, self.image.url))
        return 'no file'
    __str__.allow_tags = True


class CategoryImage(CategoryManufacturerImage):
    """
    Класс изображения для категории товара
    """
    class Meta:
        db_table = 'category_image'
        verbose_name = 'Изображение категории'
        verbose_name_plural = 'Изображения категорий'

    category = models.OneToOneField('Category')


class ManufacturerLogo(CategoryManufacturerImage):
    """
    Класс изображения (логотип) для производителя
    """
    class Meta:
        db_table = 'manufacturer_logo'
        verbose_name = 'Логотип производителя'
        verbose_name_plural = 'Логотипы производителя'

    manufacturer = models.OneToOneField('Manufacturer')


class Manufacturer(models.Model):
    """
    Класс производителя товара
    """
    class Meta:
        db_table = 'manufacturer'
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    manufacturer_title = models.CharField(max_length=100, verbose_name='Название', blank=False, unique=True)
    manufacturer_slug = models.CharField(max_length=100, verbose_name='URL')
    manufacturer_text = models.TextField(max_length=1000, verbose_name='Описание производителя', blank=True)
    manufacturer_country = models.CharField(max_length=50, verbose_name='Страна производства')

    def __str__(self):
        return self.manufacturer_title

    def __unicode__(self):
        return self.manufacturer_title


class Category(MPTTModel):
    """
    Класс категории товара.
    Категории могут иметь подкатегории и так далее
    """
    class Meta:
        db_table = 'category'
        verbose_name = 'Товарная группа'
        verbose_name_plural = 'Товарные группы'

    class MPTTMeta:
        order_insertion_by = ['category_title']

    category_title = models.CharField(max_length=100, verbose_name='Название', blank=False, unique=True)
    category_slug = models.CharField(max_length=100, verbose_name='URL')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                            verbose_name='Входит в группу')

    def __str__(self):
        return self.category_title

    def __unicode__(self):
        return self.category_title


class Product(models.Model):
    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    product_title = models.CharField(max_length=255, verbose_name='Название товара', blank=False, unique=True)
    product_slug = models.CharField(max_length=255, verbose_name='URL')
    product_text = RichTextField(verbose_name='Описание товара', blank=False)
    product_add_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения', blank=False)
    product_change_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    product_start_price = models.IntegerField(verbose_name='Начальная цена', default=0)
    product_start_price_in_dollars = models.BooleanField(verbose_name='Цена в долларах', default=False)
    product_current_price = models.IntegerField(verbose_name='Текущая цена', default=0)
    product_present = models.BooleanField(verbose_name='В наличии', default=True)
    product_available_for_order = models.BooleanField(verbose_name='Под заказ', default=False)
    product_size = models.CharField(verbose_name='Размер(без слова "размер")', blank=True, max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель')
    category = models.ForeignKey(Category, verbose_name='Категория товара')


class ProductImageBase(models.Model):
    """
    Абстрактный класс изображения для товара
    """
    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Метод для удаления файла с диска при удалении экземпляра класса рисунка из БД,
        работает если производить удаление именно объекта рисунка из админки,
        а не объекта производителя, категории или товара и как следствие -> каскадно
        объекта рисунка связанного с ним.
        """
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Метод для удаления файла с диска при замене старого изображения(файла)
        новым в объекте рисунка без создания нового объекта рисунка.
        Пустые папки при этом не удаляются.
        """

        if self.pk:
            old = self.__class__._default_manager.get(pk=self.pk)
            if old.image.name and (not self.image._committed or not self.image.name):
                old.image.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Формирует тэг для отображения файла в админке
        """
        if self.image:
            return mark_safe('<img src="%s%s"/>' % (SITE_ADDR, self.image.url))
        return 'no file'
    __str__.allow_tags = True


class ProductImage(ProductImageBase):
    class Meta:
        db_table = 'product_image'
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'
    """
    Изображение товара размером ширина 400 высота 300 для страницы товара
    """
    image = ProcessedImageField(upload_to='products/%Y/%m/%d',
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG')

    product = models.ForeignKey(Product, related_name='images')

    def clean(self):
        """
        Метод для валидации изображения перед сохранением (Используется Pillow).
        """
        image = self.image

        if image:
            # валидация размеров
            img = Image.open(image)
            w, h = img.size
            img_asp_ratio = float(format(w/h, '.2f'))
            my_asp_ratio = float(format(400/300, '.2f'))
            if img_asp_ratio != my_asp_ratio and (w < 400 or h < 300):
                raise ValidationError(size_validation_message_w400_h300)
        else:
            raise ValidationError(invalid_image_file_validation_message)

        return image
