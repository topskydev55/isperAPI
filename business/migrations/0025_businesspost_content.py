# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-24 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0024_auto_20190624_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesspost',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='\u5185\u5bb9'),
        ),
    ]
