# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-04 01:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0050_auto_20190504_0130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flowdocs',
            options={'ordering': ['-update_time'], 'verbose_name': '\u7d20\u6750\u6587\u6863', 'verbose_name_plural': '\u7d20\u6750\u6587\u6863'},
        ),
    ]