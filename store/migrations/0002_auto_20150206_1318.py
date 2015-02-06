# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to=store.models.make_upload_path, verbose_name='Изображение', default='', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='parentCategory',
            field=models.ForeignKey(default='', to='store.Category', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=store.models.make_upload_path, verbose_name='Изображение', default='', blank=True),
            preserve_default=True,
        ),
    ]
