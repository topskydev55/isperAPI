# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-21 15:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0047_merge_20190717_1903'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0006_studentrequestassiststatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentChatLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(blank=True, max_length=512, null=True, verbose_name='\u6d88\u606f\u5185\u5bb9')),
                ('msg_type', models.IntegerField(default=0, verbose_name='Message Type')),
                ('ext', models.TextField(verbose_name='Message Ext')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='Business')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_from', to=settings.AUTH_USER_MODEL, verbose_name='From User')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_to', to=settings.AUTH_USER_MODEL, verbose_name='To User')),
            ],
            options={
                'db_table': 't_student_chatlog',
                'verbose_name': 'StudentChatLogs',
                'verbose_name_plural': 'StudentChatLogs',
            },
        ),
    ]
