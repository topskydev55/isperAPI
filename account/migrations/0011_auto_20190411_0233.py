# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-11 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20190411_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuser',
            name='create_time',
            field=models.DateTimeField(editable=False, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]