# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-31 02:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0048_businessguide'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideChatLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(blank=True, max_length=512, null=True, verbose_name='\u6d88\u606f\u5185\u5bb9')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessGuide', verbose_name='Guide')),
            ],
            options={
                'db_table': 't_guide_chatlog',
                'verbose_name': 'GuideChatLog',
                'verbose_name_plural': 'GuideChatLog',
            },
        ),
    ]
