# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDocNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(verbose_name='\u9879\u76ee')),
                ('node_id', models.IntegerField(verbose_name='\u73af\u8282')),
                ('doc_id', models.IntegerField(verbose_name='\u7d20\u6750')),
            ],
            options={
                'db_table': 't_project_doc_node',
                'verbose_name': '\u9879\u76ee\u73af\u8282\u7d20\u6750\u5206\u914d',
                'verbose_name_plural': '\u9879\u76ee\u73af\u8282\u7d20\u6750\u5206\u914d',
            },
        ),
        migrations.AlterModelOptions(
            name='projectdocrole',
            options={'verbose_name': '\u9879\u76ee\u73af\u8282\u7d20\u6750\u89d2\u8272\u5206\u914d', 'verbose_name_plural': '\u9879\u76ee\u73af\u8282\u7d20\u6750\u89d2\u8272\u5206\u914d'},
        ),
        migrations.RemoveField(
            model_name='projectdocrole',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='projectdocrole',
            name='doc_id',
        ),
        migrations.RemoveField(
            model_name='projectdocrole',
            name='node_id',
        ),
        migrations.RemoveField(
            model_name='projectdocrole',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='projectrole',
            name='role_avatar',
        ),
        migrations.RemoveField(
            model_name='projectrole',
            name='role_file',
        ),
        migrations.AddField(
            model_name='projectdoc',
            name='file',
            field=models.FileField(default=1, upload_to=b'files/', verbose_name='\u6587\u4ef6'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectdocrole',
            name='doc_node_id',
            field=models.IntegerField(default=1, verbose_name='\u73af\u8282\u7d20\u6750'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectrole',
            name='image_id',
            field=models.IntegerField(default=1, verbose_name='\u89d2\u8272\u5f62\u8c61'),
            preserve_default=False,
        ),
    ]