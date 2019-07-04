# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-04 05:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflow', '0065_auto_20190623_1900'),
        ('business', '0033_auto_20190703_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='\u6295\u7968\u4e3b\u9898')),
                ('method', models.IntegerField(blank=True, null=True, verbose_name='\u6295\u7968\u65b9\u5f0f')),
                ('end_time', models.DateTimeField(verbose_name='\u6295\u7968\u7528\u65f6')),
                ('share', models.IntegerField(blank=True, null=True, verbose_name='\u6295\u7968\u7ed3\u679c')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='Business ID')),
            ],
            options={
                'db_table': 't_poll',
                'verbose_name': 'poll',
                'verbose_name_plural': 'poll',
            },
        ),
        migrations.CreateModel(
            name='PollMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_status', models.IntegerField(default=0, verbose_name='Poll status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Poll User ID')),
            ],
            options={
                'db_table': 't_pollMember',
                'verbose_name': 'pollMember',
                'verbose_name_plural': 'pollMember',
            },
        ),
        migrations.AddField(
            model_name='poll',
            name='members',
            field=models.ManyToManyField(to='business.PollMember', verbose_name='\u6295\u7968\u4eba\u8303\u56f4'),
        ),
        migrations.AddField(
            model_name='poll',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowNode', verbose_name='Node ID'),
        ),
    ]
