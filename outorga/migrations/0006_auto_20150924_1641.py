# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0005_auto_20150924_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='termo',
            options={'ordering': ('-ano', '-processo'), 'verbose_name': 'Termo de Outorga', 'verbose_name_plural': 'Termos de Outorga'},
        ),
    ]
