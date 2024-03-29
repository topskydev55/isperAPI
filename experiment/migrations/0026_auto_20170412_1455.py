# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0025_auto_20170411_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experimenttranspath',
            options={'ordering': ['step'], 'verbose_name': '\u5b9e\u9a8c\u6d41\u8f6c\u8def\u5f84', 'verbose_name_plural': '\u5b9e\u9a8c\u6d41\u8f6c\u8def\u5f84'},
        ),
        migrations.RenameField(
            model_name='experimenttranspath',
            old_name='cur_node_id',
            new_name='node_id',
        ),
        migrations.RemoveField(
            model_name='experimenttranspath',
            name='in_node_id',
        ),
        migrations.RemoveField(
            model_name='experimenttranspath',
            name='out_node_id',
        ),
        migrations.AddField(
            model_name='experimentdoccontent',
            name='sign',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='\u7b7e\u540d'),
        ),
        migrations.AddField(
            model_name='experimentdoccontent',
            name='sign_status',
            field=models.BooleanField(default=False, verbose_name='\u7b7e\u540d\u72b6\u6001'),
        ),
    ]
