# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0028_auto_20170331_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flownode',
            name='step',
            field=models.IntegerField(default=0, verbose_name='\u6392\u5e8f'),
        ),
    ]
