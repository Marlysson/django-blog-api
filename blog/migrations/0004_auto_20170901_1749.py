# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-01 20:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170901_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='geo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to='blog.Geo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Address'),
        ),
    ]
