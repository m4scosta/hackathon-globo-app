# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grade_parser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='program',
            field=models.ForeignKey(default=1, to='grade_parser.Program'),
            preserve_default=False,
        ),
    ]
