# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-21 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_studentchatlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentchatlog',
            name='to_user',
        ),
    ]