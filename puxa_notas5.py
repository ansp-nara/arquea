#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
from django.core.management import setup_environ
import settings
setup_environ(settings)

from outorga.models import Acordo, Item, OrigemFapesp, Termo
from financeiro.models import ExtratoCC, ExtratoFinanceiro, Pagamento, Auditoria, TipoComprovante, Estado as EstadoFinanceiro
from protocolo.models import Protocolo, Descricao, TipoDocumento, Estado as EstadoProtocolo, Origem
from membro.models import Membro
from decimal import Decimal

if len(sys.argv) < 2:
    sys.exit()
    
dados = open(sys.argv[1])

def pega_num(num):
    num = num.rstrip().lstrip()
    (i, d) = num.split(',')
    integers = i.split('.')
    i = ''
    for j in integers: i = i+j
    n = "%s.%s" % (i,d)
    return n

sem_item = 0
sem_tipo = 0
data_anterior = datetime.date(2000,01,01)
cheques = []
termo = Termo.objects.get(ano=2004,digito=2)
concluido = EstadoProtocolo.objects.get(nome=u'Concluído')
pago = EstadoFinanceiro.objects.get(nome__startswith=u'Pago e anexado')
default = TipoComprovante.objects.get(nome__contains='NF')
orig = Origem.objects.get(nome='Correio')

for l in dados:
    dt = l.rstrip().split(';')
    so_libera = False
    libera_nova = True
	
    dt[5] = pega_num(dt[5])

    (dia, mes, ano) = (int(x) for x in dt[3].split('/'))
    if ano < 2000:
        ano += 2000
    dt[3] = datetime.date(ano, mes, dia)
    liberacao = dt[1:6]
    protocolo = dt[3:6]+dt[7:8]+dt[11:12]
    pagamento = dt[2:4]+dt[5:7]+dt[8:9]
    auditoria = dt[0:2]+dt[9:11]+dt[12:13]
    
    item = Item.objects.filter(descricao__exact=pagamento[3].rstrip().lstrip(), natureza_gasto__termo=termo)
    acordo = Acordo.objects.filter(descricao__icontains=pagamento[4].rstrip().lstrip())
    origem = None
    if not item or not acordo:
        sem_item += 1
	print pagamento[3], item, pagamento[4], acordo
    else:
	try:
           origem = OrigemFapesp.objects.get(item_outorga=item[0], acordo=acordo[0])
        except:
	   print pagamento[3], item, pagamento[4], acordo
    try:
	cc = ExtratoCC.objects.get(cod_oper=pagamento[0])#, valor=Decimal(pagamento[1]))
    except:
	print "cheque não encontrado: %s\n" % pagamento[0]
	continue
	   
    descs = protocolo[3].rstrip().lstrip().split(' - ')
    emp = descs[0]
    desc = ' - '.join(descs[1:])
    try:
	descricao = Descricao.objects.get(entidade__sigla=emp, descricao=desc)
    except:
	print 'Descrição: ', emp, desc

	
    try:
	tipo = TipoDocumento.objects.get(nome__iexact=protocolo[4].rstrip().lstrip())
    except:
	tipo = TipoDocumento.objects.get(nome__iexact='NF')

    prot = Protocolo()
    prot.estado = concluido
    prot.termo = termo
    prot.descricao2 = descricao
    prot.tipo_documento = tipo
    prot.referente = protocolo[4][:100]
    prot.data_vencimento = protocolo[0]
    prot.data_chegada = protocolo[0]
    prot.origem = orig
    prot.num_documento = protocolo[1]
    prot.valor_total = Decimal(protocolo[2])
    prot.save()
      
    pgto = Pagamento()
    pgto.protocolo = prot
    pgto.conta_corrente = cc
    pgto.valor_fapesp = Decimal(pagamento[2])
    pgto.origem_fapesp = origem
      
         
    pgto.save()
        
    audit = Auditoria()
    try:
	tipo = TipoComprovante.objects.get(nome__contains=auditoria[2])
    except:
	tipo = default
	    
    try:
	est_aud = EstadoFinanceiro.objects.get(nome=auditoria[3])
    except:
	est_aud = pago
	    
    audit.estado = est_aud
    audit.pagamento = pgto
    audit.tipo = tipo
    audit.parcial = auditoria[0]
    audit.pagina = auditoria[1]
    audit.obs = auditoria[4]
    audit.save()
	
    #if not cc.extrato_financeiro:
	#cc.extrato_financeiro = libera
	#cc.save()
	#if len(cc) > 1:
	   #cc_grande += 1
        #print item, acordo, origem, cc

print sem_item
dados.close()
