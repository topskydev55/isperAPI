# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-09-13 10:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20190418_2011'),
        ('business', '0069_merge_20190911_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessBillDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_conception', models.CharField(blank=True, max_length=512, null=True, verbose_name='doc_conception')),
                ('doc_name', models.CharField(blank=True, max_length=512, null=True, verbose_name='doc_name')),
                ('doc_url', models.CharField(blank=True, max_length=512, null=True, verbose_name='doc_url')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.UploadFile', verbose_name='doc_id')),
            ],
            options={
                'db_table': 't_business_bill_doc',
                'verbose_name': 'BusinessBillDoc',
                'verbose_name_plural': 'BusinessBillDoc',
            },
        ),
        migrations.AddField(
            model_name='businessbilllist',
            name='docs',
            field=models.ManyToManyField(blank=True, to='business.BusinessBillDoc', verbose_name='docs'),
        ),
    ]
