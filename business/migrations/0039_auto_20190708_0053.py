# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-07 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0038_auto_20190705_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdoccontent',
            name='doc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.BusinessDoc', verbose_name='BusinessDoc'),
        ),
    ]