# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0016_auto_20170306_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentdoc',
            name='role_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u89d2\u8272'),
        ),
    ]