# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='\u540d\u79f0')),
                ('no', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u5e8f\u53f7')),
                ('leader', models.IntegerField(verbose_name='\u7ec4\u957f')),
                ('open_join', models.PositiveIntegerField(verbose_name='\u5f00\u653e\u9080\u8bf7')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('del_flag', models.IntegerField(choices=[(1, '\u662f'), (0, '\u5426')], default=0, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'db_table': 't_team',
                'verbose_name': '\u5c0f\u7ec4',
                'verbose_name_plural': '\u5c0f\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField(verbose_name='\u5c0f\u7ec4')),
                ('user_id', models.IntegerField(verbose_name='\u7528\u6237')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('del_flag', models.IntegerField(choices=[(1, '\u662f'), (0, '\u5426')], default=0, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'db_table': 't_team_member',
                'verbose_name': '\u5c0f\u7ec4\u6210\u5458',
                'verbose_name_plural': '\u5c0f\u7ec4\u6210\u5458',
            },
        ),
    ]