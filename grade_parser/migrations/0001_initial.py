# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('relevancy', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('key', models.IntegerField(serialize=False, primary_key=True)),
            ],
        ),
    ]
