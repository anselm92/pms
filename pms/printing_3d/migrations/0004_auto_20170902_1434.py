# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 12:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printing_3d', '0003_auto_20170902_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order3d',
            options={'permissions': (('view_order3d', 'Can view'),)},
        ),
    ]
