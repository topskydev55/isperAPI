# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import experiment.models
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0019_auto_20170331_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentrolestatus',
            name='show_times',
            field=models.IntegerField(default=0, verbose_name='\u7533\u8bf7\u5c55\u793a\u6b21\u6570'),
        ),
        migrations.AddField(
            model_name='experimentrolestatus',
            name='upload_times',
            field=models.IntegerField(default=0, verbose_name='\u7533\u8bf7\u63d0\u4ea4\u6b21\u6570'),
        ),
        migrations.AlterField(
            model_name='experimentdocsign',
            name='file',
            field=models.ImageField(blank=True, null=True, storage=utils.storage.ImageStorage(), upload_to=experiment.models.get_experiment_doc_upload_to, verbose_name='\u7b7e\u540d\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='experimentmessagefile',
            name='file',
            field=models.FileField(storage=utils.storage.FileStorage(), upload_to=experiment.models.get_experiment_doc_upload_to, verbose_name='\u6587\u4ef6'),
        ),
    ]