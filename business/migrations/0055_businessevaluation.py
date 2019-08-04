# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-08-04 04:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0054_askchatlog_sender_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=512, null=True, verbose_name='comment')),
                ('value', models.CharField(blank=True, max_length=512, null=True, verbose_name='value')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.Business', verbose_name='business')),
                ('role_alloc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.BusinessRoleAllocation', verbose_name='role_alloc')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'db_table': 't_business_evaluation',
                'verbose_name': 'BusinessEvaluation',
                'verbose_name_plural': 'BusinessEvaluation',
            },
        ),
    ]