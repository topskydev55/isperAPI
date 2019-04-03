# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import project.models
import utils.storage


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20170223_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrole',
            name='flow_role_id',
            field=models.IntegerField(default=1, verbose_name='\u6d41\u7a0b\u89d2\u8272id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdoc',
            name='file',
            field=models.FileField(blank=True, null=True, storage=utils.storage.FileStorage(), upload_to=project.models.get_project_doc_upload_to, verbose_name='\u6587\u4ef6'),
        ),
    ]