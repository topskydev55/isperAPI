# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-18 01:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0018_auto_20190612_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspositionstatus',
            name='business_role_allocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.BusinessRoleAllocation', verbose_name='Business Role Allocation'),
        ),
    ]