# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-03 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0039_tcompany_is_default'),
        ('workflow', '0048_flow_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowrole',
            name='capacity',
            field=models.IntegerField(default=1, verbose_name='\u4eba\u6570'),
        ),
        migrations.AddField(
            model_name='flowrole',
            name='job_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.TJobType'),
        ),
        migrations.AlterField(
            model_name='flowrole',
            name='category',
            field=models.PositiveIntegerField(blank=True, choices=[(1, '\u5f8b\u5e08'), (2, '\u6cd5\u5b98'), (3, '\u516c\u52a1\u5458'), (4, '\u68c0\u5bdf\u5b98'), (5, '\u516c\u8bc1\u5458'), (6, '\u7acb\u6cd5\u8005'), (99, '\u5176\u4ed6')], null=True, verbose_name='\u7c7b\u522b'),
        ),
    ]
