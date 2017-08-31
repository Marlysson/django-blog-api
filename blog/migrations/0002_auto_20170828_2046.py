# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-28 23:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='person', to='blog.Address')),
            ],
        ),
        migrations.RemoveField(
            model_name='geo',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='geo',
            name='lng',
        ),
        migrations.AddField(
            model_name='geo',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geo',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.User'),
        ),
    ]