# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-29 13:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0046_experimentreportstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experimentreportstatus',
            name='sitting_status',
        ),
    ]
