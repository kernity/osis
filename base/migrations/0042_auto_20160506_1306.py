# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-06 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_messagehistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagehistory',
            old_name='content',
            new_name='content_html',
        ),
        migrations.RemoveField(
            model_name='messagehistory',
            name='origin',
        ),
        migrations.AddField(
            model_name='messagehistory',
            name='content_txt',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messagehistory',
            name='reference',
            field=models.CharField(db_index=True, max_length=100, null=True),
        ),
    ]