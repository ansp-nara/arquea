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
termo = Termo.objects.get(ano=2007)
concluido = EstadoProtocolo.objects.get(nome=u'Concluído')
pago = EstadoFinanceiro.objects.get(nome__startswith=u'Pago e anexado')
default = TipoComprovante.objects.get(nome__contains='NF')
orig = Origem.objects.get(nome='Correio')

for l in dados:
    dt = l.rstrip().split(';')
    so_libera = False
    libera_nova = True
    try:
        dt[9] = pega_num(dt[9])
    except:
        so_libera = True	
    dt[3] = pega_num(dt[3])

    (dia, mes, ano) = (int(x) for x in dt[1].split('/'))
    if ano < 2000:
        ano += 2000
    dt[1] = datetime.date(ano, mes, dia)
    liberacao = dt[1:6]
    protocolo = dt[6:8]+dt[14:16]+dt[18:19]
    pagamento = dt[8:10]+dt[12:14]+dt[16:18]
    auditoria = dt[10:12]+dt[18:20]
    
    if liberacao[0] > data_anterior:
        data_anterior = liberacao[0]
        cheques = []
    if pagamento[0] in cheques:
	libera_nova = False
    else:
        cheques.append(pagamento[0])
        
    if libera_nova:
	libera = ExtratoFinanceiro()
	libera.termo = termo
	libera.data_libera = liberacao[0]
	libera.cod = liberacao[1]
	libera.valor = Decimal(liberacao[2])
	libera.parcial = liberacao[3]
	libera.despesa_caixa = bool(liberacao[4])
	libera.save()
    else:
        libera = list(ExtratoFinanceiro.objects.all())[-1]
        
    if not so_libera:
        (dia, mes, ano) = (int(x) for x in protocolo[1].split('/'))
	if ano < 2000:
	    ano += 2000
        protocolo[1] = datetime.date(ano, mes, dia)
        item = Item.objects.filter(descricao__icontains=pagamento[3].rstrip().lstrip(), natureza_gasto__termo=termo)
        acordo = Acordo.objects.filter(descricao__icontains=pagamento[2].rstrip().lstrip())
        origem = None
        if not item or not acordo:
            sem_item += 1
	    print pagamento[3], item, pagamento[2], acordo
        else:
            origem = OrigemFapesp.objects.get(item_outorga=item[0], acordo=acordo[0])
        try:
	    cc = ExtratoCC.objects.get(cod_oper=pagamento[0])#, valor=Decimal(pagamento[1]))
	except:
	    print "cheque não encontrado: %s" % pagamento[0]
	    continue
	   
	descs = protocolo[2].split(' - ')
	emp = descs[0]
	desc = ' - '.join(descs[1:])
	try:
	   descricao = Descricao.objects.get(entidade__sigla=emp, descricao=desc)
	except:
	   print desc, emp

	try:
	   tipo = TipoDocumento.objects.get(nome__iexact=auditoria[2].rstrip().lstrip())
	except:
	   tipo = TipoDocumento.objects.get(nome__iexact='NF')

        prot = Protocolo()
        prot.estado = concluido
        prot.termo = termo
        prot.descricao2 = descricao
        prot.tipo_documento = tipo
        prot.referente = protocolo[3][:100]
        prot.data_vencimento = protocolo[1]
        prot.data_chegada = protocolo[1]
        prot.origem = orig
        prot.num_documento = protocolo[0]
        #print prot.referente
        prot.save()
        
        pgto = Pagamento()
        pgto.protocolo = prot
        pgto.conta_corrente = cc
        pgto.valor_fapesp = Decimal(pagamento[1])
        pgto.origem_fapesp = origem
        
        if pagamento[4] == 'S':
	    pgto.reembolso = True
	    try:
                pgto.membro = Membro.objects.get(nome__startswith=pagamento[5])
            except:
	        print pagamento[5]
            
        pgto.save()
       
        audit = Auditoria()
        try:
	    tipo = TipoComprovante.objects.get(nome__contains=auditoria[2])
	except:
	    tipo = default
	    
	audit.estado = pago
	audit.pagamento = pgto
	audit.tipo = tipo
	audit.parcial = auditoria[0]
	audit.pagina = auditoria[1]
	audit.obs = auditoria[3]
	audit.save()
	
        if not cc.extrato_financeiro:
	    cc.extrato_financeiro = libera
	    #cc.save()
	#if len(cc) > 1:
	   #cc_grande += 1
        #print item, acordo, origem, cc



print sem_item
dados.close()
