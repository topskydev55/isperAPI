# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-24 22:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_tuser_tcompany'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuser',
            name='tcompany',
        ),
    ]
