# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-14 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0018_auto_20190612_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessmessage',
            name='user_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='\u59d3\u540d'),
        ),
    ]
