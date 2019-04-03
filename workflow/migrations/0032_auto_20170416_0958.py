# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-16 09:58
from __future__ import unicode_literals

from django.db import migrations, models
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0031_auto_20170414_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flow',
            name='diagram',
        ),
        migrations.AlterField(
            model_name='flowposition',
            name='code_position',
            field=models.CharField(max_length=32, verbose_name='flash\u7ad9\u4f4d'),
        ),
        migrations.AlterField(
            model_name='flowposition',
            name='position',
            field=models.CharField(max_length=32, verbose_name='\u573a\u666f\u7ad9\u4f4d'),
        ),
        migrations.AlterField(
            model_name='flowprocess',
            name='file',
            field=models.FileField(blank=True, null=True, storage=utils.storage.FileStorage(), upload_to=b'process/', verbose_name='\u573a\u666f\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='flowprocess',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=utils.storage.ImageStorage(), upload_to=b'process/', verbose_name='\u573a\u666f\u622a\u56fe'),
        ),
    ]