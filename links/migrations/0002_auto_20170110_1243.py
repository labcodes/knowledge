# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-10 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['created']},
        ),
        migrations.RenameField(
            model_name='link',
            old_name='link',
            new_name='url',
        ),
    ]