# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-08-26 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0061_businessbillpartdoc_doc_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessbillpartdoc',
            name='doc_conception',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='doc_conception'),
        ),
    ]
