# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_remove_team_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='open_join',
            field=models.PositiveIntegerField(choices=[(1, '\u5f00\u653e'), (2, '\u4e0d\u5f00\u653e')], default=1, verbose_name='\u5f00\u653e\u9080\u8bf7'),
        ),
    ]
