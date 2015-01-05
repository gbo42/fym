# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fym', '0002_auto_20150105_0742'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloco',
            name='hearts',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trilha',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloco',
            name='texto',
            field=models.CharField(unique=True, max_length=2000),
        ),
    ]
