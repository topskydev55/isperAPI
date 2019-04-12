# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-04 12:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0063_auto_20170919_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluateExperiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField(db_index=True, verbose_name='\u5b9e\u9a8cid')),
                ('user_id', models.IntegerField(verbose_name='\u7528\u6237id')),
                ('content', models.CharField(max_length=255, verbose_name='\u5185\u5bb9')),
                ('sys_score', models.CharField(max_length=32, verbose_name='\u7cfb\u7edf\u8bc4\u5206')),
                ('teacher_score', models.CharField(max_length=32, verbose_name='\u6559\u5e08\u8bc4\u5206')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('create_by_id', models.IntegerField(verbose_name='\u63d0\u4ea4\u4eba')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 't_evaluate_experiment',
                'verbose_name': '\u603b\u4f53\u8bc4\u4ef7',
                'verbose_name_plural': '\u603b\u4f53\u8bc4\u4ef7',
            },
        ),
        migrations.CreateModel(
            name='EvaluateNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.IntegerField(db_index=True, verbose_name='\u5b9e\u9a8cid')),
                ('node_id', models.IntegerField(db_index=True, verbose_name='\u73af\u8282id')),
                ('user_id', models.IntegerField(verbose_name='\u7528\u6237id')),
                ('content', models.CharField(max_length=255, verbose_name='\u5185\u5bb9')),
                ('sys_score', models.CharField(max_length=32, verbose_name='\u7cfb\u7edf\u8bc4\u5206')),
                ('teacher_score', models.CharField(max_length=32, verbose_name='\u6559\u5e08\u8bc4\u5206')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('create_by_id', models.IntegerField(verbose_name='\u63d0\u4ea4\u4eba')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 't_evaluate_node',
                'verbose_name': '\u73af\u8282\u8bc4\u4ef7',
                'verbose_name_plural': '\u73af\u8282\u8bc4\u4ef7',
            },
        ),
        migrations.CreateModel(
            name='EvaluatePool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluate_level', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=32, verbose_name='\u7b49\u7ea7')),
                ('evaluate_content', models.CharField(max_length=255, verbose_name='\u8bc4\u8bed\u6837\u672c')),
            ],
            options={
                'ordering': ['evaluate_type', 'evaluate_level'],
                'db_table': 't_evaluate_pool',
                'verbose_name': '\u8bc4\u4ef7\u6837\u672c',
                'verbose_name_plural': '\u8bc4\u4ef7\u6837\u672c',
            },
        ),
        migrations.CreateModel(
            name='EvaluateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=32, verbose_name='\u5206\u7c7b')),
            ],
            options={
                'db_table': 't_evaluate_type',
                'verbose_name': '\u8bc4\u4ef7\u5206\u7c7b',
                'verbose_name_plural': '\u8bc4\u4ef7\u5206\u7c7b',
            },
        ),
        migrations.AddField(
            model_name='evaluatepool',
            name='evaluate_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.EvaluateType', verbose_name='\u5206\u7c7b'),
        ),
    ]