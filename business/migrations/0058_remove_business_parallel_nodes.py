# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-08-16 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0057_business_parallel_nodes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='parallel_nodes',
        ),
    ]
