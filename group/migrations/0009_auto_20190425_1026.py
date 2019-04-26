# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-25 10:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0008_auto_20190423_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allgroups',
            name='groupInstructors',
            field=models.ManyToManyField(related_name='allgroups_set_instructors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='allgroups',
            name='groupManagers',
            field=models.ManyToManyField(related_name='allgroups_set', to=settings.AUTH_USER_MODEL),
        ),
    ]