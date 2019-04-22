# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-22 23:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_merge_20190422_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='TCompanyManagers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tcompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.TCompany')),
                ('tuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_company_managers',
                'verbose_name': '\u5355\u4f4d\u7ecf\u7406\u5458',
                'verbose_name_plural': '\u5355\u4f4d\u7ecf\u7406\u5458',
            },
        ),
    ]
