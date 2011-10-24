#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, urllib
import cookielib
from django.core.management import setup_environ
import settings
setup_environ(settings)
from financeiro.models import *
import sys

try:
  parcial = int(sys.argv[1])
except:
  print 'Uso: %s <parcial>, e parcial deve ser inteiro' % sys.argv[0]
  sys.exit()

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)
data = urllib.urlencode([('username', 'lflopez'), ('password', 'latakia414')])
req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/Login.do', data=data)
urllib2.urlopen(req)

financeiros = ExtratoFinanceiro.objects.filter(termo__id=13, parcial=parcial)
        
data = urllib.urlencode([('processo', '2010/52277-8'), ('parcial', parcial), ('tipoPrestacao', 'PRN'), ('tipoDespesa', 'REL'), ('Prosseguir', 'Prosseguir')])
req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar', data=data)
p = urllib2.urlopen(req)

dt = []
for f in financeiros:
    valor = f.valor
    if valor < Decimal('0.0'):
       valor = -valor
    try:
        int, dec = str(valor).split('.')
    except:
        int = str(valor)
	dec = 0

    if f.cod == 'PGMP':
        codigo = 'L' 
    else:
        codigo = 'D'

    dt += [('dataOperacao', f.data_libera.strftime('%d/%m/%Y')), ('operacao', codigo), ('valorOperacao', '%s,%s' % (int, dec))]

for k in range(0, 8):
    dt += [('dataOperacao', ''), ('operacao', ''), ('valorOperacao', '')]
	    
i = 0
while i < financeiros.count():
    print dt[3*i:3*i+27]
    data = urllib.urlencode(dt[3*i:3*i+27]+[('method', 'Incluir')])
    req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineIncluiVld.do?method=Incluir', data=data)
    p2 = urllib2.urlopen(req)
    #print p2.read()

    i += 9

