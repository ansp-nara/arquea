# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0003_auto_20150811_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templatert',
            options={'verbose_name': 'Template Reserva T\xe9cnica', 'verbose_name_plural': 'Templates Reserva T\xe9cnica'},
        ),
        migrations.AlterField(
            model_name='item',
            name='rt',
            field=models.BooleanField(default=False, verbose_name='Reserva t\xe9cnica?'),
        ),
    ]
