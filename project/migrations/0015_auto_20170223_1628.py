# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_auto_20170220_1026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-create_time', '-update_time'], 'verbose_name': '\u5b9e\u9a8c\u9879\u76ee', 'verbose_name_plural': '\u5b9e\u9a8c\u9879\u76ee'},
        ),
        migrations.AddField(
            model_name='projectdoc',
            name='is_initial',
            field=models.BooleanField(default=False, verbose_name='\u521d\u59cb\u7d20\u6750'),
        ),
    ]