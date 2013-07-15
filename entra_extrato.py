#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

import sys
from datetime import date
import re
from decimal import Decimal
from financeiro.models import ExtratoCC

if len(sys.argv) < 2:
    sys.exit("Nome de arquivo faltando")

arq = open(sys.argv[1])

for l in arq:
    dados = l.split()
    data = dados.pop(0)
    sinal = dados.pop()
    valor = dados.pop()
    codigo = dados.pop()
    historico = ' '.join(dados)
    (d, m, y) = map(int, data.split('/'))
    data = date(y,m,d)
    valor = re.sub('\.', '', valor)
    valor = re.sub(',', '.', valor)
    codigo = re.sub('\.', '', codigo)
    sinal = '' if sinal=='C' else '-'
    ex = ExtratoCC.objects.create(data_oper=data, cod_oper=codigo, valor=Decimal('%s%s' % (sinal, valor)), historico=historico)

