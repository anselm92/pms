# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-03 18:02
from __future__ import unicode_literals

import django.core.files.storage
import django.core.validators
from django.db import migrations, models
import printing.handlers


class Migration(migrations.Migration):

    dependencies = [
        ('printing', '0022_auto_20170902_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='file',
            field=models.FileField(default=None, null=True, storage=django.core.files.storage.FileSystemStorage(location='/opt/pms/'), upload_to=printing.handlers.order_files_upload_handler, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'stl'])]),
        ),
    ]
