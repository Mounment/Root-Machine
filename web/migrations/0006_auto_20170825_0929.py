# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-25 01:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_task_tasklogdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostgroup',
            name='bind_hosts',
            field=models.ManyToManyField(to='web.BindHost'),
        ),
    ]
