# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dollar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dollar_to_hrn', models.FloatField(max_length=6, verbose_name='Курс')),
                ('dollar_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата установки курса')),
                ('dollar_active', models.BooleanField(default=True, verbose_name='Текущий курс')),
            ],
            options={
                'db_table': 'dollar',
                'verbose_name': 'Курс доллара',
                'verbose_name_plural': 'Курсы доллара',
            },
        ),
        migrations.CreateModel(
            name='PriceIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priceIndexValue', models.FloatField(max_length=6, verbose_name=' ')),
                ('priceIndex_fromStartPrice', models.BooleanField(default=False, verbose_name='От начальной цены')),
                ('priceIndex_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата установки индекса')),
                ('priceIndex_active', models.BooleanField(default=True, verbose_name='Текущий индекс')),
            ],
            options={
                'db_table': 'priceIndex',
                'verbose_name': 'Индекс повышения цены',
                'verbose_name_plural': 'Индексы повышения цены',
            },
        ),
    ]
