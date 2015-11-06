# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0006_auto_20150924_1641'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('natureza_gasto__termo', 'descricao'), 'verbose_name': 'Item do Or\xe7amento', 'verbose_name_plural': 'Itens do Or\xe7amento'},
        ),
    ]
