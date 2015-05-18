# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('identificacao', '0003_auto_20150517_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identificacao',
            name='historico',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 18, 5, 14, 842493), verbose_name='Hist\xf3rico', editable=False),
            preserve_default=True,
        ),
    ]
