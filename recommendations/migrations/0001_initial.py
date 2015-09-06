# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FBUser',
            fields=[
                ('fb_id', models.BigIntegerField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('relevancy', models.FloatField()),
                ('user', models.ForeignKey(to='recommendations.FBUser')),
            ],
        ),
    ]
