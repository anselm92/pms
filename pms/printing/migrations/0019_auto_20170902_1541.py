# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 13:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printing', '0018_auto_20170902_1515'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomGroupFilters',
            new_name='CustomGroupFilter',
        ),
    ]
