#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)
from patrimonio.models import *
from financeiro.models import Pagamento
from identificacao.models import EnderecoDetalhe
import csv
import datetime


planilha = csv.reader(open('/tmp/dc4.csv', 'rb'), delimiter=';', quotechar='"')

i = 2
ok = []
for item in planilha:
    p = Patrimonio.objects.filter(ns=item[5],modelo=item[0].decode('iso-8859-1').encode('utf-8'))
    if p.count() == 1:
        p = p[0]
        print 'Atual: %s, %s, %s' % (p.ns, p.historico_atual().endereco, p.historico_atual().estado)
        print 'Novo: %s, %s, %s' % (item[5], item[27:30], item[22])
        print 'Seq: %s' % i
        ok.append(i)
    i += 1

print '======================================================================'

planilha = csv.reader(open('/tmp/dc4.csv', 'rb'), delimiter=';', quotechar='"')

i = 2
for item in planilha:
    if i in ok: 
        i += 1
        continue
    p = Patrimonio.objects.filter(descricao__contains=item[6])
    if p.count() == 1:
        p = p[0]
        print 'Atual: %s, %s, %s' % (p.ns, p.historico_atual().endereco, p.historico_atual().estado)
        print 'Novo: %s, %s, %s' % (item[5], item[27:30], item[22])
        print 'Seq: %s' % i
        ok.append(i)
    i += 1

print '======================================================================'

planilha = csv.reader(open('/tmp/dc4.csv', 'rb'), delimiter=';', quotechar='"')

i = 2
for item in planilha:
    if i in ok:
        i += 1
        continue
    p = Patrimonio.objects.filter(descricao=item[19].decode('iso-8859-1').encode('utf-8'))
    if p.count() == 1:
        p = p[0]
        print 'Atual: %s, %s, %s' % (p.ns, p.historico_atual().endereco, p.historico_atual().estado)
        print 'Novo: %s, %s, %s' % (item[5], item[27:30], item[22])
        print 'Seq: %s' % i
        ok.append(i)
    i += 1

print '======================================================================'

planilha = csv.reader(open('/tmp/dc4.csv', 'rb'), delimiter=';', quotechar='"')

i = 2
for item in planilha:
    if i in ok:
        i += 1
        continue
    p = Patrimonio.objects.filter(ns=item[5])
    if p.count() == 1:
        p = p[0]
        print 'Atual: %s, %s, %s' % (p.ns, p.historico_atual().endereco, p.historico_atual().estado)
        print 'Novo: %s, %s, %s' % (item[5], item[27:30], item[22])
        print 'Seq: %s' % i
        ok.append(i)
    i += 1

print len(ok)
