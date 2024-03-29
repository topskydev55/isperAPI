# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-08 10:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0041_tuser_tposition'),
    ]

    operations = [
        migrations.CreateModel(
            name='TCompanyChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(default=b'', max_length=256)),
                ('sAgree', models.IntegerField(default=0)),
                ('tAgree', models.IntegerField(default=0)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.TCompany')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_company_change',
            },
        ),
    ]
