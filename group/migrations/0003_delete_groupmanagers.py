# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-18 19:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_groups_default'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GroupManagers',
        ),
    ]