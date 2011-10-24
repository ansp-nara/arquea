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
         'STB_OUT':'STB',
         'DIA':'MNT'}
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)
data = urllib.urlencode([('username', 'lflopez'), ('password', 'latakia414')])
req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/Login.do', data=data)
urllib2.urlopen(req)

pagamentos = Pagamento.objects.filter(protocolo__termo__id=13)
pagtos = pagamentos

for p in pagamentos:
    if p.auditoria_set.filter(parcial=parcial).count() <= 0:
        pagtos = pagtos.exclude(id=p.id)
        
pagamentos = pagtos
mods = []
for m in pagamentos.values_list('origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla', flat=True).distinct():
    if not m in mods:
        mods.append(m)

if 'MPN' in mods:
   mods.remove('MPN')

for m in mods:
        
    data = urllib.urlencode([('processo', '2010/52277-8'), ('parcial', parcial), ('tipoPrestacao', 'PRN'), ('tipoDespesa', TIPOS[m]), ('Prosseguir', 'Prosseguir')])
    req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar', data=data)
    p = urllib2.urlopen(req)

    pgs = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla=m)
 
    dt = []
    for pg in pgs:
	try:
	  int, dec = str(pg.valor_fapesp).split('.')
	except:
	  int = str(pg.valor_fapesp)
	  dec = 0

        nf = pg.protocolo.num_documento
        if pg.protocolo.tipo_documento.nome.lower().find('anexo') == 0:
	    nf = '%s %s' % (pg.protocolo.tipo_documento.nome, nf)
	dt += [('notaFiscal', nf), ('dataNotaFiscal', pg.protocolo.data_vencimento.strftime('%d/%m/%Y')), ('cheque', pg.conta_corrente.cod_oper), ('pagina', pg.auditoria_set.filter(parcial=parcial).values_list('pagina', flat=True)[0]), ('valorItem', '%s,%s' % (int, dec))]

    for k in range(0, 4):
	dt += [('notaFiscal', ''), ('dataNotaFiscal', ''), ('cheque', ''), ('pagina', ''), ('valorItem', '')]
	    
    i = 0
    while i < pgs.count():
        #print dt[5*i:5*i+25]
        data = urllib.urlencode(dt[5*i:5*i+25]+[('method', 'Incluir')])
        req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineIncluiOud.do?method=Incluir', data=data)
	p2 = urllib2.urlopen(req)

	txt = p2.read()

        if txt.find('Erros') >= 0:
	   print 'Erro encontrado na inserção dos itens abaixo'
	   print dt[5*i:5*i+25]

	i += 5

