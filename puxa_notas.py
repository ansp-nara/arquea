#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
from django.core.management import setup_environ
import settings
setup_environ(settings)

from decimal import Decimal
from identificacao.models import Identificacao, Entidade, Contato
from protocolo.models import Protocolo, TipoDocumento, Origem, Estado as EstadoProtocolo
from outorga.models import Termo, Acordo, OrigemFapesp, Estado as EstadoOutorga, Natureza_gasto, Modalidade, Item as ItemOutorga
from financeiro.models import FontePagadora, Estado as EstadoFinanceiro, AuditoriaFapesp

tp, cr = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
ori, cr = Origem.objects.get_or_create(nome='Sem registro')
esp, cr = EstadoProtocolo.objects.get_or_create(nome=u'Concluído')
termo = Termo.objects.get(ano=2004, processo=14414, digito=2)
esf, cr = EstadoFinanceiro.objects.get_or_create(nome='Pago')
esa, cr = EstadoFinanceiro.objects.get_or_create(nome=u'Concluído')
eso, cr = EstadoOutorga.objects.get_or_create(nome='Ativo')
cont_default = Contato.objects.get(nome='Atendente')
ent_default = Entidade.objects.get(sigla='NARA')

dados = open('/tmp/Processo_04_14414-2_MODELO_SISTEMA.csv')

for l in dados:
    dt = l.rstrip().split(';')
    valor = dt[8]
    if not valor:
      print dt
      continue
    try:
      (lixo, valor) = valor.split('R$ ')
    except:
      print "Valor: ", valor
      sys.exit()
    (i, d) = valor.split(',')
    integers = i.split('.')
    i = ''
    for j in integers: i = i+j
    n = "%s.%s" % (i,d[:2])
    dt[8] = n

    (dia, mes, ano) = (int(x) for x in dt[6].split('/'))
    dt[6] = datetime.date(ano, mes, dia)
    descricao = dt[12]

    #.split(' - ')

    #if len(descr) > 1:
      #descricao = ' - '.join(descr[1:])
      #identifica = descr[0]
    #else:
      #identifica = dt[9]
      #descricao = dt[10]

    ndocs = dt[7].split(',')
    if len(ndocs) > 1:
      obs = dt[13] + ' outras notas: ' + ','.join(ndocs[1:])
    else:
      obs = dt[13]
    ndoc = ndocs[0]

    entidade = dt[10]
    contato = dt[11]
    if entidade:
        ent, cr = Entidade.objects.get_or_create(sigla=entidade[:20].upper(), defaults={'nome':entidade, 'ativo':True, 'cnpj':'', 'url':''})
    else:
	ent = ent_default
    if contato:
	cont, cr = Contato.objects.get_or_create(nome=contato, defaults={'tel':'xxxxxx', 'ativo':True})
    else:
	cont = cont_default

    ident, cr = Identificacao.objects.get_or_create(entidade=ent, contato=cont, defaults={'area':'', 'funcao':'', 'ativo':True})

    try: 
      testando = descricao[:200].decode('utf-8')
      descricao = descricao[:200]
    except UnicodeDecodeError, e:
      descricao = descricao[:199]

    p = Protocolo.objects.create(tipo_documento=tp, identificacao=ident, origem=ori, termo=termo, num_documento=ndoc, data_chegada=dt[6], 
	  valor_total=Decimal(dt[8]), moeda_estrangeira=False, descricao=descricao, obs=obs, estado=esp)
    p.save()

    try:
	pagina = int(dt[4])
    except:
	pagina = int(dt[4][:dt[4].index('*')])

    af = AuditoriaFapesp.objects.create(estado=esa, parcial=1, pagina=pagina)
    af.save()
    ac, cr = Acordo.objects.get_or_create(descricao=dt[2], defaults={'estado':eso})

    ng = Natureza_gasto.objects.get(modalidade__sigla=dt[1], termo=termo)
    item, cr = ItemOutorga.objects.get_or_create(descricao=dt[3], defaults={'natureza_gasto':ng, 'justificativa':' ', 'quantidade':0}) 
    of, cr = OrigemFapesp.objects.get_or_create(acordo=ac, item_outorga=item)
    fp = FontePagadora(estado=esf, protocolo=p, valor=Decimal(dt[8]), parecer='', origem_fapesp=of)
    fp.save()
dados.close()
