# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printing', '0002_order_order_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
