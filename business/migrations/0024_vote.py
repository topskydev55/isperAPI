# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-24 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0064_flowroleallocation_image_id'),
        ('business', '0023_voteitem_votemember'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.IntegerField(verbose_name='Vote Mode')),
                ('title', models.TextField(verbose_name='Vote Title')),
                ('description', models.TextField(verbose_name='Vote Description')),
                ('method', models.IntegerField(verbose_name='Vote Method')),
                ('end_time', models.DateTimeField(verbose_name='Vote End Time')),
                ('max_vote', models.IntegerField(verbose_name='Vote Max Count')),
                ('lost_vote', models.IntegerField(verbose_name='Vote Lost Count')),
                ('items', models.ManyToManyField(to='business.VoteItem', verbose_name='Vote Items')),
                ('members', models.ManyToManyField(to='business.VoteMember', verbose_name='Vote Members')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.FlowNode', verbose_name='Node ID')),
            ],
            options={
                'db_table': 't_vote',
                'verbose_name': 'vote',
                'verbose_name_plural': 'vote',
            },
        ),
    ]