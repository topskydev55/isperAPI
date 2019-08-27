# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-08-25 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0059_auto_20190825_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessbillchapter',
            name='sections',
            field=models.ManyToManyField(blank=True, to='business.BusinessBillSection', verbose_name='sections'),
        ),
        migrations.AlterField(
            model_name='businessbilllist',
            name='chapters',
            field=models.ManyToManyField(blank=True, to='business.BusinessBillChapter', verbose_name='chapters'),
        ),
        migrations.AlterField(
            model_name='businessbillpart',
            name='part_docs',
            field=models.ManyToManyField(blank=True, to='business.BusinessBillPartDoc', verbose_name='part_docs'),
        ),
        migrations.AlterField(
            model_name='businessbillsection',
            name='parts',
            field=models.ManyToManyField(blank=True, to='business.BusinessBillPart', verbose_name='parts'),
        ),
    ]
