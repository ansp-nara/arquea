# -*- coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from outorga.models import Termo
from protocolo.models import Protocolo, ItemProtocolo
from financeiro.models import Pagamento
#from financeiro.models import Despesa
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib import admin
from django.http import Http404, HttpResponse
#from utils.functions import pega_lista
from django.utils import simplejson
#from models import FontePagadora, AuditoriaInterna, AuditoriaFapesp
#from decimal import Decimal
from django.db.models import Max
from identificacao.models import Entidade, EnderecoDetalhe


# Gera uma lista dos protocolos conforme o termo selecionado.
def escolhe_termo(request):
    if request.method == 'POST':
        retorno = []
         
        t = request.POST.get('id')
        termo = Termo.objects.get(pk=int(t))
        protocolos = Protocolo.objects.filter(termo=termo)

        for p in protocolos:
            descricao = '%s: %s - %s' % (p.doc_num(), p.descricao2.__unicode__(), p.mostra_valor())
            retorno.append({'pk':p.pk, 'valor':descricao})
        
        if not retorno:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]
    else:
        retorno = [{"pk":"0","valor":"Nenhum registro"}]

    json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")



# Gera uma lista dos itens do protocolo conforme protocolo selecionado.
def escolhe_protocolo(request):
    if request.method == 'POST':
        retorno = []
        id = request.POST.get('id')
        previous = request.POST.get('previous')

        if id and previous:
            t = Termo.objects.get(pk=int(previous))
            itens = ItemProtocolo.objects.filter(protocolo__id=int(id), protocolo__termo=t)

            for i in itens:
                descricao = '%s - %s (%s)' % (i.quantidade, i.descricao, i.mostra_valor())
                retorno.append({'pk':i.pk, 'valor': descricao})

            if not retorno:
                retorno = [{"pk":"0","valor":"Nenhum registro"}]
        else:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")


def escolhe_pagamento(request):
    if request.method == 'POST':
        retorno = []
        termo = request.POST.get('termo')
        numero = request.POST.get('numero')
        
        if termo and numero:
	    pgt = Pagamento.objects.filter(protocolo__termo__id=termo)
	    from django.db.models import Q
	    for p in pgt.filter(Q(conta_corrente__cod_oper__icontains=numero)|Q(protocolo__num_documento__icontains=numero)):
	        descricao = 'Doc. %s, cheque %s, valor %s' % (p.protocolo.num_documento,p.conta_corrente.cod_oper, p.valor_fapesp)
	        retorno.append({'pk':p.pk, 'valor':descricao})
	        
	if not retorno:
	    retorno = [{"pk":"0","valor":"Nenhum registro"}]
	    
	json = simplejson.dumps(retorno)
    else:
        raise Http404
    return HttpResponse(json, mimetype="application/json")


def escolhe_entidade(request):
    if request.method == 'POST':
        ent_id = request.POST.get('entidade')
	entidade = get_object_or_404(Entidade, pk=ent_id)

	retorno = []
	for ed in EnderecoDetalhe.objects.filter(endereco__entidade=entidade):
	    descricao = '%s - %s' % (ed.endereco.__unicode__(), ed.complemento)
	    retorno.append({'pk':ed.pk, 'valor':descricao})

        if not retorno:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    else:
        raise Http404
    return HttpResponse(json, mimetype="application/json")

