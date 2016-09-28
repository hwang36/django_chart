# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='View_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.CharField(max_length=10, null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('kwh', models.DecimalField(null=True, max_digits=15, decimal_places=10, blank=True)),
                ('power', models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True)),
            ],
        ),
    ]
