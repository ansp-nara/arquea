# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rede', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='canal',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='enlaceoperadora',
            options={'ordering': ('enlace', 'operadora')},
        ),
        migrations.AlterModelOptions(
            name='interface',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='midia',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='projeto',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='segmento',
            options={'ordering': ('enlace', 'operadora')},
        ),
        migrations.AlterModelOptions(
            name='sistema',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='tipointerface',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='unidade',
            options={'ordering': ('nome',)},
        ),
        migrations.AlterModelOptions(
            name='uso',
            options={'ordering': ('nome',)},
        ),
    ]
