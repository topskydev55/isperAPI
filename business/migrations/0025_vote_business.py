# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-24 23:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0024_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='business',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='Business ID'),
            preserve_default=False,
        ),
    ]
