# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0006_auto_20170206_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flownode',
            name='task_id',
            field=models.CharField(max_length=16, verbose_name='xml\u4e2dtask id'),
        ),
        migrations.AlterField(
            model_name='flowprocess',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, '\u52a8\u753b'), (2, '\u7f16\u8f91\u5fc3\u5f97'), (3, '\u67e5\u770b\u8d44\u6599'), (4, '\u751f\u6210\u5b9e\u9a8c\u62a5\u544a')], verbose_name='\u7c7b\u578b:\u52a8\u753b,\u7f16\u8f91\u5fc3\u5f97,\u67e5\u770b\u6750\u6599,\u751f\u6210\u5b9e\u9a8c\u62a5\u544a'),
        ),
    ]
