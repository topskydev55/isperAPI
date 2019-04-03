# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0020_auto_20170405_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experimentrolestatus',
            name='show_times',
        ),
        migrations.RemoveField(
            model_name='experimentrolestatus',
            name='upload_times',
        ),
        migrations.AddField(
            model_name='experimentrolestatus',
            name='show_status',
            field=models.PositiveIntegerField(choices=[(1, '\u5df2\u540c\u610f'), (2, '\u672a\u540c\u610f'), (9, '\u672a\u5904\u7406')], default=9, verbose_name='\u5c55\u793a\u72b6\u6001'),
        ),
        migrations.AddField(
            model_name='experimentrolestatus',
            name='submit_status',
            field=models.PositiveIntegerField(choices=[(1, '\u672a\u63d0\u4ea4'), (2, '\u5df2\u63d0\u4ea4'), (9, '\u672a\u5904\u7406')], default=9, verbose_name='\u63d0\u4ea4\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='experimentdoc',
            name='submit_status',
            field=models.PositiveIntegerField(choices=[(1, '\u672a\u63d0\u4ea4'), (2, '\u5df2\u63d0\u4ea4'), (9, '\u672a\u5904\u7406')], default=9, verbose_name='\u63d0\u4ea4\u72b6\u6001'),
        ),
    ]