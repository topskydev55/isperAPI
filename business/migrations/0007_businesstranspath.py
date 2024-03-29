# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-05 02:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0040_merge_20190603_2340'),
        ('workflow', '0057_flow_created_role'),
        ('business', '0006_business_officeitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessTransPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(blank=True, max_length=16, null=True, verbose_name='xml\u4e2dtask id')),
                ('step', models.IntegerField(blank=True, default=1, null=True, verbose_name='\u6b65\u9aa4')),
                ('control_status', models.PositiveIntegerField(choices=[(1, '\u672a\u542f\u52a8'), (2, '\u542f\u52a8')], default=1, verbose_name='\u8868\u8fbe\u7ba1\u7406\u72b6\u6001')),
                ('vote_status', models.PositiveIntegerField(choices=[(1, '\u8fdb\u884c\u4e2d'), (2, '\u5df2\u7ed3\u675f')], default=1, verbose_name='\u6295\u7968\u72b6\u6001')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='\u4efb\u52a1')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowNode', verbose_name='\u5f53\u524d\u73af\u8282')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='\u5f53\u524d\u9879\u76ee')),
            ],
            options={
                'ordering': ['step'],
                'db_table': 't_business_trans_path',
                'verbose_name': '\u5b9e\u9a8c\u6d41\u8f6c\u8def\u5f84',
                'verbose_name_plural': '\u5b9e\u9a8c\u6d41\u8f6c\u8def\u5f84',
            },
        ),
    ]
