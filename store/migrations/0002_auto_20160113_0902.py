# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-13 07:02
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='products/%Y/%m/%d')),
            ],
            options={
                'db_table': 'product_image',
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товара',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='productText',
            field=ckeditor.fields.RichTextField(default=111, verbose_name='Описание товара'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='other/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='manufacturerlogo',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='other/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.Product'),
        ),
    ]