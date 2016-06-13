# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membro', '0002_auto_20150811_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='historico',
            name='carga_horaria',
            field=models.IntegerField(default=8, null=True, verbose_name='Carga hor\xe1ria', blank=True),
        ),
    ]
