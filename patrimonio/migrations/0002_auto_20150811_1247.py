# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipamento',
            name='ean',
        ),
        migrations.RemoveField(
            model_name='equipamento',
            name='ncm',
        ),
        migrations.RemoveField(
            model_name='patrimonio',
            name='cfop',
        ),
        migrations.RemoveField(
            model_name='patrimonio',
            name='ncm',
        ),
        migrations.RemoveField(
            model_name='patrimonio',
            name='ocst',
        ),
    ]
