# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-20 09:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20170820_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostgroup',
            old_name='hosts',
            new_name='bind_hosts',
        ),
    ]
