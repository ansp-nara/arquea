# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controle',
            name='membro',
            field=models.ForeignKey(verbose_name='Membro', to='membro.Membro'),
        ),
    ]
