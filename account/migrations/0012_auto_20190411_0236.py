# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-11 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20190411_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuser',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='tuser',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
    ]
