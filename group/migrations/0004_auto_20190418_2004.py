# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-18 20:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0003_delete_groupmanagers'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupManagers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 't_groupManagers',
            },
        ),
        migrations.RemoveField(
            model_name='groups',
            name='groupManager_ids',
        ),
        migrations.AddField(
            model_name='groupmanagers',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.Groups'),
        ),
        migrations.AddField(
            model_name='groupmanagers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]