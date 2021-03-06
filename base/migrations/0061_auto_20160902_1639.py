# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0005_auto_20160902_1639'),
        ('base', '0060_offeryeardomain'),
    ]

    operations = [
        migrations.AddField(
            model_name='offeryear',
            name='grade_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reference.GradeType'),
        ),
        migrations.AddField(
            model_name='offeryeardomain',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reference.Domain'),
        ),
        migrations.AddField(
            model_name='offeryeardomain',
            name='offer_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.OfferYear'),
        ),
    ]
