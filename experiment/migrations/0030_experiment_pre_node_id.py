# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0029_experimenttranspath_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='pre_node_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u4e0a\u4e00\u6b65\u73af\u8282'),
        ),
    ]