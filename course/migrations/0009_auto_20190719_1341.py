# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-19 05:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_course_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universitylinkedcompany',
            name='seted_company_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seted_company_manager', to='account.TCompanyManagers'),
        ),
    ]