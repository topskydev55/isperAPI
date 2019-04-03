# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import experiment.models
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0040_auto_20170425_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentdoccontent',
            name='file',
            field=models.FileField(blank=True, null=True, storage=utils.storage.FileStorage(), upload_to=experiment.models.get_experiment_doc_upload_to, verbose_name='\u6587\u4ef6'),
        ),
    ]