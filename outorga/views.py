# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from outorga.models import Termo, Modalidade, Item, Natureza_gasto, Acordo
from django.utils import simplejson
from utils.functions import render_to_pdf
from decimal import Decimal
from identificacao.models import *
from financeiro.models import Pagamento
from django.contrib.auth.decorators import permission_required, login_required
from django.template import RequestContext

def termo(request, termo_id):

    """

    """
    
    u = request.user
    if not u.is_authenticated():
        return admin.site.login(request)
    
    #if not u.has_perm('outorga.change_termo'):
     #   raise PermissionDenied

    t = get_object_or_404(Termo, pk=termo_id)
    
    r = []
    for p in t.outorga_set.all():
        r.append(p)
            
    return render_to_response('outorga/termo.html',
                              {'termo' : t,
                               'pedido' : r})

                            
             
def pedido(request, pedido_id):

    """

    """

    u = request.user
    if not u.is_authenticated():
        return admin.site.login(request)
    
    #if not u.has_perm('outorga.change_termo'):
    #    raise PermissionDenied
    
    p = get_object_or_404(Outorga, pk=pedido_id)
    
    return render_to_response('outorga/pedido.html',
                              {'pedido' : p})



# Gera uma lista com as modalidades do termo selecionado.
def escolhe_termo(request):
    if request.method == 'POST':
        termo = int(request.POST.get('id'))

        retorno = {}

        if termo:
	    retorno['modalidade'] = []
            retorno['item'] = []
            
 	    t = Termo.objects.get(pk=termo)
            modalidades = Modalidade.modalidades_termo(t)
            itens = Item.objects.filter(natureza_gasto__termo=t, item=None)
 
            for m in modalidades:
                retorno['modalidade'].append({'pk':m.pk, 'valor':m.__unicode__()})
            for i in itens:
                retorno['item'].append({'pk':i.pk, 'valor':i.__unicode__()})

            if not retorno['modalidade']:
                retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
            if not retorno['item']:
                retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
	else:
            retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
            retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")



# Gera uma lista dos itens de outorga conforme a modalidade selecionada.
def escolhe_modalidade(request):
    if request.method == 'POST':
        retorno = []
        id = request.POST.get('id')
        previous = request.POST.get('previous')

        if id and previous:
            t = Termo.objects.get(pk=int(previous))
            itens = Item.objects.filter(natureza_gasto__termo=t, natureza_gasto__modalidade=id, item=None)

            for i in itens:
                retorno.append({'pk':i.pk, 'valor':i.__unicode__()})

            if not retorno:
                retorno = [{"pk":"0","valor":"Nenhum registro"}]
        else:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")


def seleciona_termo_natureza(request):
    if request.method == 'POST':
        termo = int(request.POST.get('id'))

        retorno = []

        if termo:
    
            t = Termo.objects.get(pk=termo)
            
            naturezas = Natureza_gasto.objects.filter(termo=t)
            
            for n in naturezas:
                retorno.append({'pk':n.pk, 'valor':n.modalidade.sigla})
            if not retorno:
                retorno = [{"pk":"0","valor":"Nenhum registro"}]
        else:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")


# Gera listas modalidade, item e natureza conforme termo selecionado.
def seleciona_mod_item_natureza(request):
    if request.method == 'POST':
        termo = int(request.POST.get('id'))

        retorno = {}

        if termo:
            retorno['modalidade'] = []
            retorno['item'] = []
            retorno['natureza'] = []
	    
            t = Termo.objects.get(pk=termo)
            
            modalidade = Modalidade.modalidades_termo(t)
            itens = Item.objects.filter(natureza_gasto__termo=t, item=None)
            naturezas = Natureza_gasto.objects.filter(termo=t)
            
            for m in modalidade:
                retorno['modalidade'].append({'pk':m.pk, 'valor':m.__unicode__()})
            for i in itens:
                retorno['item'].append({'pk':i.pk, 'valor':i.__unicode__()})
            for n in naturezas:
                retorno['natureza'].append({'pk':n.pk, 'valor':n.__unicode__()})

            
            if not retorno['modalidade']:
                retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
            if not retorno['item']:
                retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
            if not retorno['natureza']:
                retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]
        else:
            retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
            retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
            retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")



# Gera uma lista dos itens de outorga conforme a modalidade selecionada.
def seleciona_item_natureza(request):
    if request.method == 'POST':
        retorno = {}

        id = request.POST.get('id')
        previous = request.POST.get('previous')

        if id and previous:
            retorno['item'] = []
            retorno['natureza'] = []

            t = Termo.objects.get(pk=int(previous))
            itens = Item.objects.filter(natureza_gasto__termo=t, natureza_gasto__modalidade=id, item=None)
            naturezas = Natureza_gasto.objects.filter(termo=t, modalidade=id)

            for i in itens:
                retorno['item'].append({'pk':i.pk, 'valor':i.__unicode__()})
            for n in naturezas:
                retorno['natureza'].append({'pk':n.pk, 'valor':n.__unicode__()})


            if not retorno['item']:
                retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
            if not retorno['natureza']:
                retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]
        else:
            retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
            retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")


def gastos_acordos(request):
    acordos = []
    acordo = ['']
    for t in Termo.objects.filter(ano__gte=2005).order_by('ano'):
        acordo.append('%s (%s)' % (t.__unicode__(), t.duracao_meses()))
        
    acordos.append(acordo)
    for a in Acordo.objects.all():
 
        acordo = [a.descricao]
        for t in Termo.objects.filter(ano__gte=2005).order_by('ano'):
            total = Decimal('0.0')
            for o in a.origemfapesp_set.filter(item_outorga__natureza_gasto__termo=t):
                total += o.gasto()
            acordo.append(total)
        acordos.append(acordo)

    return render_to_pdf('outorga/acordos.pdf', {'acordos':acordos})

@login_required
def contratos(request):
    
    entidades = []
    for e in Entidade.objects.order_by('sigla'):
        cts = e.contrato_set.order_by('-data_inicio')
        if cts.count():
            entidade = {'entidade':e.sigla}
            contratos = []
            for c in cts:
                contrato = {'inicio':c.data_inicio, 'termino':c.limite_rescisao, 'numero':c.numero, 'arquivo':c.arquivo, 'auto':c.auto_renova}
                oss = c.ordemdeservico_set.order_by('-data_inicio')
                if oss.count():
                   ordens = []
                   for os in oss:
                       ordens.append(os)
                   contrato.update({'os':ordens})
                contratos.append(contrato)
            entidade.update({'contratos':contratos})
            entidades.append(entidade)

    return render_to_response('outorga/contratos.html', {'entidades':entidades})
   

@login_required 
def por_item(request):
    if request.method == 'GET':
        termo = request.GET.get('termo')
        entidade = request.GET.get('entidade')

        itens = Item.objects.filter(natureza_gasto__termo__id=termo)
        if entidade:
            itens = itens.filter(entidade__id=entidade)

        its = []
        for i in itens:
            it = {'item':i}
            pgs = []
            for p in Pagamento.objects.filter(origem_fapesp__item_outorga=i):
                pgs.append(p)
            it.update({'pgtos':pgs})
            its.append(it)

        retorno = RequestContext(request)
        retorno.update({'itens':its})
        return render_to_response('outorga/por_item.html', retorno)

@login_required
def relatorio_termos(request):
    if request.method == 'GET':
        termos = Termo.objects.order_by('-ano')
        return render_to_response('outorga/termos.html', {'termos':termos})
