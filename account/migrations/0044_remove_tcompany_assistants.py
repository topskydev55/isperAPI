# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-09 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0043_auto_20190508_2101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tcompany',
            name='assistants',
        ),
    ]
