# -*- coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from outorga.models import Termo
from protocolo.models import Protocolo, ItemProtocolo
from financeiro.models import Pagamento
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib import admin
from django.http import Http404, HttpResponse
#from utils.functions import pega_lista
from django.utils import simplejson
#from models import FontePagadora, AuditoriaInterna, AuditoriaFapesp
#from decimal import Decimal
from django.db.models import Max
from identificacao.models import Entidade, EnderecoDetalhe, Endereco
from models import *
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, login_required

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
	        if p.conta_corrente:
	            descricao = 'Doc. %s, cheque %s, valor %s' % (p.protocolo.num_documento,p.conta_corrente.cod_oper, p.valor_fapesp)
		else:
		    descricao = 'Doc. %s, valor %s' % (p.protocolo.num_documento, p.valor_patrocinio)

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


def patrimonio_existente(request):
    if request.method == 'POST':
        retorno = {'marca':'', 'modelo':'', 'descricao':'', 'procedencia':''}
        part_number = request.POST.get('part_number')
        
        existentes = Patrimonio.objects.filter(part_number__iexact=part_number)

        if part_number and existentes.count():
            p = existentes[0]
            retorno = {'marca':p.marca, 'modelo':p.modelo, 'descricao':p.descricao, 'procedencia':p.procedencia}

        json = simplejson.dumps(retorno)
    else:
        raise Http404
    
    return HttpResponse(json, mimetype='application/json')

@login_required
def por_estado(request):
    if request.method == 'POST':
        if request.POST.get('estado'):
            estado_id = request.POST.get('estado')
            estado = get_object_or_404(Estado, pk=estado_id)

            no_estado = []
            for p in Patrimonio.objects.filter(contido__isnull=True):
                ht = p.historico_atual()
                if ht and ht.estado == estado:
                    no_estado.append(ht.id)

            no_estado = HistoricoLocal.objects.filter(id__in=no_estado)
            entidades_ids = no_estado.values_list('endereco__endereco__entidade', flat=True).distinct()
            entidades = []
            for e in Entidade.objects.filter(id__in=entidades_ids):
                detalhes = []
                detalhes_ids = no_estado.values_list('endereco', flat=True).filter(endereco__endereco__entidade=e)
                for d in EnderecoDetalhe.objects.filter(id__in=detalhes_ids):
                    detalhes.append({'detalhe':d, 'patrimonio':Patrimonio.objects.filter(historicolocal__in=no_estado.filter(endereco=d))})
                entidades.append({'entidade':e, 'detalhes':detalhes})
            return render_to_response('patrimonio/por_estado.html', {'estado':estado, 'entidades':entidades})
    else:
        return render_to_response('patrimonio/sel_estado.html', {'estados':Estado.objects.all()}, context_instance=RequestContext(request))

@login_required
def por_local(request):
    if request.method == 'POST':
        atuais = []
        for p in Patrimonio.objects.filter(contido__isnull=True):
            ht = p.historico_atual()
            if ht:
                 atuais.append(ht.id)

        detalhe_id = request.POST.get('detalhe')
        if detalhe_id:
            detalhe = get_object_or_404(EnderecoDetalhe, pk=detalhe_id)
            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco=detalhe)
            return render_to_response('patrimonio/por_local.html', {'detalhe':detalhe, 'detalhes':[{'patrimonio':Patrimonio.objects.filter(historicolocal__in=historicos)}]})
        else:
            endereco_id = request.POST.get('endereco')
            endereco = get_object_or_404(Endereco, pk=endereco_id)

            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__endereco=endereco)
            detalhes = []
            detalhes_ids = historicos.values_list('endereco', flat=True).filter(endereco__endereco=endereco)
            for d in EnderecoDetalhe.objects.filter(id__in=detalhes_ids):
                detalhes.append({'detalhe':d, 'patrimonio':Patrimonio.objects.filter(historicolocal__in=historicos.filter(endereco=d))})
            return render_to_response('patrimonio/por_local.html', {'endereco':endereco, 'detalhes':detalhes})
    else:
        return render_to_response('patrimonio/sel_local.html', {'entidades':Entidade.objects.all()}, context_instance=RequestContext(request))

