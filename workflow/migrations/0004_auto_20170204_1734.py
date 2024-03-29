# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_auto_20170120_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowNodeDocs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_id', models.IntegerField(verbose_name='\u6d41\u7a0b')),
                ('node_id', models.IntegerField(verbose_name='\u73af\u8282')),
                ('doc_id', models.IntegerField(verbose_name='\u7d20\u6750')),
            ],
            options={
                'db_table': 't_flow_node_docs',
                'verbose_name': '\u6d41\u7a0b\u73af\u8282\u7d20\u6750\u5206\u914d',
                'verbose_name_plural': '\u6d41\u7a0b\u73af\u8282\u7d20\u6750\u5206\u914d',
            },
        ),
        migrations.RemoveField(
            model_name='flowdocs',
            name='node_id',
        ),
        migrations.AddField(
            model_name='flowdocs',
            name='flow_id',
            field=models.IntegerField(default=1, verbose_name='\u6d41\u7a0b'),
            preserve_default=False,
        ),
    ]
