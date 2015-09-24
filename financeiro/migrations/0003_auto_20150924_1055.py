# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_auto_20150811_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extratocc',
            name='cod_oper',
            field=models.IntegerField(help_text='C\xf3digo com m\xe1ximo de 10 d\xedgitos.', verbose_name='Documento', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
