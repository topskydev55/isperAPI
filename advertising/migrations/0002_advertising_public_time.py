# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-05 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertising', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertising',
            name='public_time',
            field=models.DateTimeField(null=True, verbose_name='\u65f6\u95f4'),
        ),
    ]