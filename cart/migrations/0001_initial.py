# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-10 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_person', models.CharField(max_length=100, verbose_name='Фамилия Имя Отчество покупателя')),
                ('order_person_phone', models.CharField(max_length=30, verbose_name='Контактный телефон')),
                ('order_person_address', models.CharField(max_length=200, verbose_name='Адрес доставки')),
                ('order_person_email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('order_pay_option', models.CharField(choices=[('Предоплата на карту', 'Предоплата'), ('Наложный платеж', 'Наложный платеж'), ('Оплата курьеру', 'Оплата курьеру'), ('Оплата в магазине', 'Оплата в магазине')], default=None, max_length=30, verbose_name='Тип оплаты')),
                ('order_delivery_option', models.CharField(choices=[('Самовывоз из магазина', 'Самовывоз из магазина'), ('Новая Почта', 'Новая Почта'), ('Доставка курьером', 'Доставка курьером')], default=None, max_length=30, verbose_name='Тип доставки')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')),
                ('order_delivered', models.BooleanField(default=False, verbose_name='Заказ выполнен')),
                ('order_confirmed', models.BooleanField(default=False, verbose_name='Заказ подтвержден')),
                ('order_products', models.CharField(blank=True, max_length=200, verbose_name='Заказанные товары')),
                ('order_code', models.CharField(default=2697, max_length=4, verbose_name='Код заказа')),
                ('order_sum', models.IntegerField(default=0, verbose_name='Сумма заказа')),
            ],
            options={
                'verbose_name_plural': 'Заказы',
                'verbose_name': 'Заказ',
                'db_table': 'order',
            },
        ),
    ]
