# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0002_auto_20150517_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateRT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o')),
                ('modalidade', models.ForeignKey(to='outorga.Modalidade')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='rt',
            field=models.BooleanField(default=False),
        ),
    ]
