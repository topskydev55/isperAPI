# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-15 21:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0048_tnotifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tcompanymanagerassistants',
            name='actions',
        ),
        migrations.RemoveField(
            model_name='tcompanymanagerassistants',
            name='tcompany',
        ),
        migrations.RemoveField(
            model_name='tcompanymanagerassistants',
            name='tuser',
        ),
        migrations.RemoveField(
            model_name='tcompany',
            name='assistants',
        ),
        migrations.DeleteModel(
            name='TCompanyManagerAssistants',
        ),
    ]