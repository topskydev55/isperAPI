# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-09-11 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0066_merge_20190911_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='parallel_count',
            field=models.IntegerField(default=0, null=True, verbose_name='parallel count'),
        ),
    ]