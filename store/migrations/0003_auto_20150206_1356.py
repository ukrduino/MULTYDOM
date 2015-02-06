# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20150206_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parentCategory',
            field=models.ForeignKey(to='store.Category', null=True, blank=True),
            preserve_default=True,
        ),
    ]
