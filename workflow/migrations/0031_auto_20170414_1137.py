# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0030_auto_20170414_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowroleaction',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowAction', verbose_name='\u529f\u80fd\u52a8\u4f5c'),
        ),
    ]
