# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-14 05:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0068_auto_20190714_1048'),
        ('business', '0043_merge_20190710_2345'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectDecideResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_role_allocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessRoleAllocation', verbose_name='Business Role Allocation')),
                ('selectedItems', models.ManyToManyField(to='workflow.SelectDecideItem', verbose_name='Selected Items')),
            ],
            options={
                'db_table': 't_selectDecideResult',
                'verbose_name': 'selectDecideResult',
                'verbose_name_plural': 'selectDecideResult',
            },
        ),
    ]