# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_projectdocrole_project_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectdocrole',
            name='doc_node_id',
        ),
        migrations.AddField(
            model_name='projectdocrole',
            name='doc_id',
            field=models.IntegerField(default=1, verbose_name='\u7d20\u6750'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectdocrole',
            name='node_id',
            field=models.IntegerField(default=1, verbose_name='\u73af\u8282'),
            preserve_default=False,
        ),
    ]
