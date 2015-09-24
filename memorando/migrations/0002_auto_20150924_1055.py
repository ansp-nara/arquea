# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorando', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memorandosimples',
            options={'ordering': ('-data', '-numero'), 'verbose_name_plural': 'Memorandos Simples'},
        ),
    ]
