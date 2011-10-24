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

TIPOS = {'STB':'STC',
         'DET':'STR',
	 'MCN':'MCS',
	 'MPN':'MPE',
         'DIA':'MNT',
	 'REL':'REL'}

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)
data = urllib.urlencode([('username', 'lflopez'), ('password', 'latakia414')])
req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/Login.do', data=data)
urllib2.urlopen(req)

mods = ['STB', 'DET', 'MCN', 'MPN', 'DIA', 'REL']
#mods = ['MPN']
        
for m in mods:
        
    data = urllib.urlencode([('processo', '2010/52277-8'), ('parcial', parcial), ('tipoPrestacao', 'PRN'), ('tipoDespesa', TIPOS[m]), ('Prosseguir', 'Prosseguir')])
    req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar', data=data)
    p = urllib2.urlopen(req)

    data = urllib.urlencode([('method', 'Excluir')])
    req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineResumo.do', data=data)
    p2 = urllib2.urlopen(req)

    txt = p2.read()
    x = txt.split('<a href="PconlineResumo.do?id=')
    for t in x[1:]:
        (n, lixo) = t.split('method=Excluir">')
	r = n.split('&')
	n = r[0]

        if m == 'REL':
	    tp = 'Vld'
	elif m == 'MPN':
	    tp = 'Mpe'
	else:
	    tp = 'Oud'
	req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineExclui%s.do?method=Excluir&id=%s' % (tp,n))
	p3 = urllib2.urlopen(req)

