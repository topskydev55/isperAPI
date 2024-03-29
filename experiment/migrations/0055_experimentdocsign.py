# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-01 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0054_experimenttranspath_vote_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentDocSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField(verbose_name='\u5b9e\u9a8cid')),
                ('node_id', models.IntegerField(verbose_name='\u73af\u8282id')),
                ('doc_id', models.IntegerField(verbose_name='\u4e0a\u4f20\u6587\u6863id')),
                ('role_id', models.IntegerField(verbose_name='\u89d2\u8272')),
                ('sign', models.CharField(blank=True, max_length=18, null=True, verbose_name='\u7b7e\u540d')),
                ('sign_status', models.PositiveIntegerField(choices=[(1, '\u5df2\u7b7e\u5b57'), (2, '\u62d2\u7edd\u7b7e\u5b57')], default=1, verbose_name='\u7b7e\u540d\u72b6\u6001')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'db_table': 't_experiment_doc_sign',
                'verbose_name': '\u5b9e\u9a8c\u73af\u8282\u6587\u6863\u7b7e\u5b57\u8bb0\u5f55',
                'verbose_name_plural': '\u5b9e\u9a8c\u73af\u8282\u6587\u6863\u7b7e\u5b57\u8bb0\u5f55',
            },
        ),
    ]
