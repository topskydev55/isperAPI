# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-07-31 02:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0049_guidechatlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidechatlog',
            name='sender',
            field=models.ForeignKey(default=1605, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Tuser'),
            preserve_default=False,
        ),
    ]
