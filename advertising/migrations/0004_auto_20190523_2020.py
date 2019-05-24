# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-23 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertising', '0003_auto_20190505_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertising',
            name='path',
        ),
        migrations.AddField(
            model_name='advertising',
            name='path_docx',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u6587\u4ef6\u8def\u5f841'),
        ),
        migrations.AddField(
            model_name='advertising',
            name='path_html',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u6587\u4ef6\u8def\u5f842'),
        ),
    ]