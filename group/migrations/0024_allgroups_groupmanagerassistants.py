# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-15 22:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0023_auto_20190515_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='allgroups',
            name='groupManagerAssistants',
            field=models.ManyToManyField(related_name='allgroups_set_assistants', to=settings.AUTH_USER_MODEL),
        ),
    ]