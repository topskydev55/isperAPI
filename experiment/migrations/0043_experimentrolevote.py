# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-13 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0042_experimentpositionstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentRoleVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField(verbose_name='\u5b9e\u9a8c')),
                ('node_id', models.IntegerField(verbose_name='\u73af\u8282')),
                ('user_id', models.IntegerField(blank=True, null=True, verbose_name='\u7528\u6237')),
                ('role_id', models.IntegerField(verbose_name='\u89d2\u8272')),
                ('path_id', models.IntegerField(blank=True, null=True, verbose_name='\u5b9e\u9a8c\u8def\u5f84')),
                ('status', models.PositiveIntegerField(choices=[(1, '\u672a\u63d0\u4ea4'), (2, '\u5df2\u63d0\u4ea4'), (9, '\u672a\u5904\u7406')], default=9, verbose_name='\u6295\u7968\u72b6\u6001')),
            ],
            options={
                'db_table': 't_experiment_role_vote',
                'verbose_name': '\u5b9e\u9a8c\u6295\u7968\u73af\u8282',
                'verbose_name_plural': '\u5b9e\u9a8c\u6295\u7968\u73af\u8282',
            },
        ),
    ]
