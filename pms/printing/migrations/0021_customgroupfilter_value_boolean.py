# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printing', '0020_auto_20170902_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='customgroupfilter',
            name='value_boolean',
            field=models.BooleanField(default=False),
        ),
    ]