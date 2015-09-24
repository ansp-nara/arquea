# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estado',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='tipocomprovantefinanceiro',
            options={'ordering': ('nome',), 'verbose_name': 'Tipo de Comprovante Financeiro', 'verbose_name_plural': 'Tipos de Comprovante Financeiro'},
        ),
    ]
