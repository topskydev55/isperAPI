# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-08-16 10:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_auto_20190722_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='universitylinkedcompany',
            options={'ordering': ['-create_time'], 'verbose_name': 'UniversityLinkedCompany', 'verbose_name_plural': 'UniversityLinkedCompany'},
        ),
    ]
