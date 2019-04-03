# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 17:41
from __future__ import unicode_literals

from django.db import migrations, models
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20170204_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdoc',
            name='file',
            field=models.FileField(blank=True, null=True, storage=utils.storage.FileStorage(), upload_to=b'files/', verbose_name='\u6587\u4ef6'),
        ),
    ]