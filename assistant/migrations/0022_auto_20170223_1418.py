# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-23 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0021_auto_20170209_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewer',
            name='is_phd_supervisor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='academicassistant',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_supervisor', to='assistant.Reviewer'),
        ),
    ]
