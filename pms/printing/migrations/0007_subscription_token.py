# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 07:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printing', '0006_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='token',
            field=models.CharField(default='34', max_length=30),
            preserve_default=False,
        ),
    ]
