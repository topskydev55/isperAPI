# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-08 21:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0020_merge_20190508_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tgroupmanagerassistants',
            name='action',
        ),
        migrations.RemoveField(
            model_name='tgroupmanagerassistants',
            name='permission',
        ),
    ]
