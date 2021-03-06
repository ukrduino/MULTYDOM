from django.db import models
import random


class Order(models.Model):
    """
    Класс заказа
    """

    P1 = "Предоплата на карту"
    P2 = "Наложный платеж"
    P3 = "Оплата курьеру"
    P4 = "Оплата в магазине"
    D1 = "Самовывоз из магазина"
    D2 = "Новая Почта"
    D3 = "Доставка курьером"

    PAY_CHOISES = ((P1, "Предоплата"), (P2, "Наложный платеж"), (P3, "Оплата курьеру"), (P4, "Оплата в магазине"),)
    DELIV_CHOISES = ((D1, "Самовывоз из магазина"), (D2, "Новая Почта"), (D3, "Доставка курьером"),)

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    order_person = models.CharField(max_length=100, verbose_name='Фамилия Имя Отчество покупателя', blank=False)
    order_person_phone = models.CharField(max_length=30, verbose_name='Контактный телефон', blank=False)
    order_person_address = models.CharField(max_length=200, verbose_name='Адрес доставки', blank=False)
    order_person_email = models.EmailField(verbose_name='E-mail', blank=False)
    order_pay_option = models.CharField(max_length=30, verbose_name='Тип оплаты', blank=False, default=None, choices=PAY_CHOISES)
    order_delivery_option = models.CharField(max_length=30, verbose_name='Тип доставки',
                                             blank=False, default=None, choices=DELIV_CHOISES)
    order_date = models.DateTimeField(verbose_name='Дата размещения', auto_now_add=True)
    order_delivered = models.BooleanField(verbose_name='Заказ выполнен', default=False)
    order_confirmed = models.BooleanField(verbose_name='Заказ подтвержден', default=False)
    order_products = models.CharField(max_length=200, verbose_name='Заказанные товары', blank=True)
    order_code = models.CharField(max_length=4, verbose_name='Код заказа', default=random.randint(0, 10000))
    order_sum = models.IntegerField(verbose_name='Сумма заказа', default=0)

# при обращении к классу Order возвращает его код
    def __unicode__(self):
        return self.order_code
