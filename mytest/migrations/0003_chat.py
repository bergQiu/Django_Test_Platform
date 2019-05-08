# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-04-12 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mytest', '0002_auto_20181013_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=20)),
                ('sendto', models.CharField(max_length=20)),
                ('ip_from', models.CharField(max_length=20)),
                ('ip_to', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]