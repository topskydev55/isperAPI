# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-19 01:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0021_businessexperience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessdocsign',
            name='node',
        ),
    ]