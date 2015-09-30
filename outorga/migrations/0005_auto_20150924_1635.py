# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0004_auto_20150903_1000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='termo',
            options={'ordering': ('-ano', 'processo'), 'verbose_name': 'Termo de Outorga', 'verbose_name_plural': 'Termos de Outorga'},
        ),
    ]
