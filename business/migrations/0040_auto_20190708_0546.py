# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-07 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0039_auto_20190708_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdoccontent',
            name='sign',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7b7e\u540d'),
        ),
    ]