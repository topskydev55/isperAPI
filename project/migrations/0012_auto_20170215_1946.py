# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20170208_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, '\u7acb\u6cd5\u5b9e\u9a8c'), (2, '\u6267\u6cd5\u5b9e\u9a8c'), (3, '\u8bc9\u8bbc\u4e0e\u4ef2\u88c1\u5b9e\u9a8c'), (4, '\u975e\u8bc9\u4e1a\u52a1\u5b9e\u9a8c'), (5, '\u6cd5\u5f8b\u5b9e\u6548\u8bc4\u4ef7\u5b9e\u9a8c'), (6, '\u8bc1\u636e\u5b66\u5b9e\u9a8c'), (7, '\u6cd5\u5f8b\u601d\u7ef4\u5b9e\u9a8c'), (8, '\u81ea\u7531\u7c7b\u578b\u5b9e\u9a8c')], default=1, verbose_name='\u5b9e\u9a8c\u7c7b\u578b'),
        ),
    ]
