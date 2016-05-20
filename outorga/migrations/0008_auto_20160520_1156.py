# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0007_auto_20150924_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termo',
            name='processo',
            field=models.CharField(default=b'0', help_text='ex. 52885', max_length=15, verbose_name='Processo', validators=[django.core.validators.RegexValidator(b'^[0-9]+$', 'Somente digitos s\xe3o permitidos.')]),
        ),
    ]
