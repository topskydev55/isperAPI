# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-02 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0055_auto_20190526_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowroleallocation',
            name='can_start',
            field=models.BooleanField(default=False, verbose_name='Can Start the business'),
        ),
    ]