# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 11:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0022_delete_experimentdocsign'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExperimentSpeak',
        ),
    ]
