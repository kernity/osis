# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-22 10:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_triggers_field_changed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offeryear',
            old_name='offer_parent',
            new_name='parent',
        ),
    ]
