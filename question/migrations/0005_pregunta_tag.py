# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 04:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_auto_20170320_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='tag',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='question.Tag'),
            preserve_default=False,
        ),
    ]