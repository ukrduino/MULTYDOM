# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import store.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Название', max_length=100, unique=True)),
                ('slug', models.CharField(verbose_name='URL', max_length=100)),
                ('image', models.ImageField(upload_to=store.models.make_upload_path, verbose_name='Изображение', default='')),
                ('parentCategory', models.ForeignKey(to='store.Category')),
            ],
            options={
                'verbose_name': 'Товарная группа',
                'db_table': 'category',
                'verbose_name_plural': 'Товарные группы',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Название', max_length=100, unique=True)),
                ('slug', models.CharField(verbose_name='URL', max_length=100)),
                ('image', models.ImageField(upload_to=store.models.make_upload_path, verbose_name='Изображение', default='')),
                ('manufacturerText', models.TextField(verbose_name='Описание производителя', max_length=1000)),
                ('manufacturerCountry', models.CharField(verbose_name='Страна производства', max_length=50)),
            ],
            options={
                'verbose_name': 'Производитель',
                'db_table': 'manufacturer',
                'verbose_name_plural': 'Производители',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Название', max_length=100, unique=True)),
                ('slug', models.CharField(verbose_name='URL', max_length=100)),
                ('image', models.ImageField(upload_to=store.models.make_upload_path, verbose_name='Изображение', default='')),
                ('productText', models.TextField(verbose_name='Описание товара')),
                ('productDate', models.DateTimeField(verbose_name='Дата размещения', auto_now_add=True)),
                ('productDateChange', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('productCurrentPrice', models.IntegerField(verbose_name='Текущая цена', default=0)),
                ('productPresence', models.BooleanField(verbose_name='В наличии', default=True)),
                ('productForOrder', models.BooleanField(verbose_name='Под заказ', default=False)),
                ('productSize', models.CharField(blank=True, verbose_name='Размер', max_length=100)),
                ('productCategory', models.ForeignKey(related_name='products', to='store.Category')),
                ('productManufacturer', models.ForeignKey(related_name='products', to='store.Manufacturer')),
            ],
            options={
                'verbose_name': 'Товар',
                'db_table': 'product',
                'verbose_name_plural': 'Товары',
            },
            bases=(models.Model,),
        ),
    ]
