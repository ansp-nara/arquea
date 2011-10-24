#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from django.core.management import setup_environ
import settings
setup_environ(settings)
from decimal import Decimal
from financeiro.models import ExtratoCC


def quebra(tp):
    d,m,y = map(int, tp[0].split('/'))
    dt = datetime.date(y,m,d)
    i, d = tp[-1].split(',')
    mil = i.split('.')
    i = ''.join(mil)
    v = '%s.%s' % (i, d)
    return (dt, tp[1], tp[2], Decimal(v))
  
f = open('/tmp/extratos/Extrato_2006.csv')

for l in f:
    (dt, cod, hist, v) = quebra(l.rstrip().split(';'))
    ex = ExtratoCC()
    ex.data_oper = dt
    ex.cod_oper = cod
    ex.historico = hist
    ex.valor = v
    ex.save()
    
