#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, urllib
import cookielib
from django.core.management import setup_environ
import settings
setup_environ(settings)
from financeiro.models import *
from patrimonio.models import *
import sys
import time

try:
  parcial = int(sys.argv[1])
except:
  print 'Uso: %s <parcial>, e parcial deve ser inteiro' % sys.argv[0]
  sys.exit()

TIPOS = {'MPN':'MPE'}
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)
data = urllib.urlencode([('username', 'lflopez'), ('password', 'latakia414')])
req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/Login.do', data=data)
urllib2.urlopen(req)

data = urllib.urlencode([('processo', '2010/52277-8'), ('parcial', parcial), ('tipoPrestacao', 'PRN'), ('tipoDespesa', 'MPE'), ('Prosseguir', 'Prosseguir')])
req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar', data=data)
p = urllib2.urlopen(req)

eqs = {}
patrimonios = Patrimonio.objects.filter(pagamento__protocolo__termo__id=13, pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla='MPN')
for e in patrimonios.filter(agilis=True):
    texto = '%s - %s - %s' % (e.modelo, e.pagamento.id, e.marca)
    if e.pagamento.auditoria_set.filter(parcial=parcial).count() == 0: continue
    if texto in eqs.keys():
        eqs[texto].append(e)
    else:
        eqs[texto] = [e]

dt = []

for eq in eqs.keys():
    qtd = len(eqs[eq])
    e = eqs[eq][0]
    pg = e.pagamento

    try:
        int, dec = str(e.valor).split('.')
    except:
        int = str(e.valor)
        dec = 0

    nf = pg.protocolo.num_documento
    sn = ','.join([pt.ns for pt in eqs[eq]])
    print eq
    modelo, pgto, marca = eq.split(' - ')
    for pt in patrimonios.filter(agilis=False, modelo=modelo, pagamento__id=pgto, marca=marca):
        sn += ',%s' % pt.ns
    if len(sn) > 170: sn = sn[:170]

    if pg.protocolo.tipo_documento.nome.lower().find('anexo') == 0:
        nf = '%s %s' % (pg.protocolo.tipo_documento.nome, nf)
    dt = [('notaFiscal', nf), ('dataNotaFiscal', pg.protocolo.data_vencimento.strftime('%d/%m/%Y')), ('cheque', pg.conta_corrente.cod_oper), ('pagina', pg.auditoria_set.filter(parcial=parcial).values_list('pagina', flat=True)[0]), ('valorItem', '%s,%s' % (int, dec)), ('descricao', e.descricao), ('quantidade', qtd), ('marca', e.marca or ''), ('modelo', e.modelo or ''), ('observacao', sn), ('procedencia', e.procedencia or '')]

    data = urllib.urlencode(dt+[('method', 'Incluir')])
    req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineIncluiOuAlteraMpe.do?method=Incluir', data=data)
    p2 = urllib2.urlopen(req)
    txt = p2.read()	

    time.sleep(60)
    if txt.find('Erros') >= 0:
        print 'Erro encontrado na inserç ã o dos itens abaixo'
        print dt


