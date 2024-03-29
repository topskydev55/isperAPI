# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0033_auto_20170420_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessRoleAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('del_flag', models.IntegerField(choices=[(1, '\u662f'), (0, '\u5426')], default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workflow.ProcessAction', verbose_name='\u573a\u666f\u52a8\u753b\u52a8\u4f5c')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Flow', verbose_name='\u6d41\u7a0b')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowNode', verbose_name='\u73af\u8282')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowRole', verbose_name='\u89d2\u8272')),
            ],
            options={
                'db_table': 't_process_role_action',
                'verbose_name': '\u89d2\u8272\u573a\u666f\u52a8\u753b',
                'verbose_name_plural': '\u89d2\u8272\u573a\u666f\u52a8\u753b',
            },
        ),
    ]
