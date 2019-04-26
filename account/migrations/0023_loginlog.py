# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-26 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_auto_20190425_1026'),
        ('account', '0022_merge_20190426_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('login_ip', models.CharField(blank=True, max_length=20, null=True, verbose_name='ip')),
                ('del_flag', models.IntegerField(choices=[(1, '\u662f'), (0, '\u5426')], default=0, verbose_name='\u662f\u5426\u5220\u9664')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.TCompany')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.AllGroups')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.TRole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 't_login_logs',
                'verbose_name': '\u767b\u5f55\u8bb0\u5f55',
                'verbose_name_plural': '\u767b\u5f55\u8bb0\u5f55',
            },
        ),
    ]