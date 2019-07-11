# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-08 01:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0065_auto_20190623_1900'),
        ('business', '0038_auto_20190705_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessDocTeamStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.IntegerField(default=1, verbose_name='Permission')),
                ('status', models.IntegerField(default=0, verbose_name='Status')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='Business')),
                ('business_doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessDoc', verbose_name='BusinessDoc')),
                ('business_team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessTeamMember', verbose_name='Business')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowNode', verbose_name='\u73af\u8282')),
            ],
            options={
                'db_table': 't_business_doc_team_status',
                'verbose_name': 'BusinessDocTeamStatus',
                'verbose_name_plural': 'BusinessDocTeamStatus',
            },
        ),
        migrations.CreateModel(
            name='BusinessStepStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField(default=1, verbose_name='\u6b65\u9aa4')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='Business')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowNode', verbose_name='\u73af\u8282')),
            ],
            options={
                'db_table': 't_business_step_status',
                'verbose_name': 'BusinessStepStatus',
                'verbose_name_plural': 'BusinessStepStatus',
            },
        ),
        migrations.AlterField(
            model_name='businessdoccontent',
            name='doc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='business.BusinessDoc', verbose_name='BusinessDoc'),
        ),
        migrations.AlterField(
            model_name='businessdoccontent',
            name='sign',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7b7e\u540d'),
        ),
    ]
