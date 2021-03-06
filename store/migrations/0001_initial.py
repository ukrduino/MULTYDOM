# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-10 11:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import imagekit.models.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('category_slug', models.CharField(max_length=100, verbose_name='URL')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.Category', verbose_name='Входит в группу')),
            ],
            options={
                'verbose_name': 'Товарная группа',
                'db_table': 'category',
                'verbose_name_plural': 'Товарные группы',
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='C:\\Users\\Sergey\\PycharmProjects\\MULTYDOM\\media\\other')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.Category')),
            ],
            options={
                'verbose_name': 'Изображение категории',
                'db_table': 'category_image',
                'verbose_name_plural': 'Изображения категорий',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer_title', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('manufacturer_slug', models.CharField(max_length=100, verbose_name='URL')),
                ('manufacturer_text', models.TextField(blank=True, max_length=1000, verbose_name='Описание производителя')),
                ('manufacturer_country', models.CharField(max_length=50, verbose_name='Страна производства')),
            ],
            options={
                'verbose_name': 'Производитель',
                'db_table': 'manufacturer',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='ManufacturerLogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='C:\\Users\\Sergey\\PycharmProjects\\MULTYDOM\\media\\other')),
                ('manufacturer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.Manufacturer')),
            ],
            options={
                'verbose_name': 'Логотип производителя',
                'db_table': 'manufacturer_logo',
                'verbose_name_plural': 'Логотипы производителя',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=255, unique=True, verbose_name='Название товара')),
                ('product_slug', models.CharField(max_length=255, verbose_name='URL')),
                ('product_add_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')),
                ('product_change_date', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('product_start_price', models.IntegerField(default=0, verbose_name='Начальная цена')),
                ('product_start_price_in_dollars', models.BooleanField(default=False, verbose_name='Цена в долларах')),
                ('product_current_price', models.IntegerField(default=0, verbose_name='Текущая цена')),
                ('product_present', models.BooleanField(default=True, verbose_name='В наличии')),
                ('product_available_for_order', models.BooleanField(default=False, verbose_name='Под заказ')),
                ('product_size', models.CharField(blank=True, max_length=100, verbose_name='Размер(без слова "размер")')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Category', verbose_name='Категория товара')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Товар',
                'db_table': 'product',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
