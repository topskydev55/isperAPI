# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_project_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_time',
            field=models.DateField(blank=True, null=True, verbose_name='\u5f00\u653e\u7ed3\u675f\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_time',
            field=models.DateField(blank=True, null=True, verbose_name='\u5f00\u653e\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]