# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0003_auto_20170523_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtube',
            name='yt_channel_id',
            field=models.CharField(default='Video Description', max_length=100),
        ),
    ]
