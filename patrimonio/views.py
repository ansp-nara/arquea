# -*- coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from outorga.models import Termo, Modalidade, Natureza_gasto, Item
from protocolo.models import Protocolo, ItemProtocolo
from financeiro.models import Pagamento
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib import admin
from django.http import Http404, HttpResponse
from utils.functions import render_to_pdf
from django.utils import simplejson
#from models import FontePagadora, AuditoriaInterna, AuditoriaFapesp
#from decimal import Decimal
from django.db.models import Max, Q
from identificacao.models import Entidade, EnderecoDetalhe, Endereco
from models import *
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, login_required
from django.template.response import TemplateResponse
from django.db.models import Q
import itertools
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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


def escolhe_detalhe(request):
    if request.method == 'POST':
        ed_id = request.POST.get('detalhe')
        detalhe = get_object_or_404(EnderecoDetalhe, pk=ed_id)

        retorno = []
        for ed in EnderecoDetalhe.objects.filter(detalhe=detalhe):
            retorno.append({'pk':ed.pk, 'valor':ed.__unicode__()})

        json = simplejson.dumps(retorno)
    else:
        raise Http404
    return HttpResponse(json, mimetype="application/json")

def escolhe_entidade(request):
    if request.method == 'POST':
        ent_id = request.POST.get('entidade')
	entidade = get_object_or_404(Entidade, pk=ent_id)

        retorno = []
	for ed in EnderecoDetalhe.objects.all():
	    if ed.end.entidade == entidade:
    	        #descricao = '%s - %s' % (ed.end.__unicode__(), ed.complemento)
                descricao = ed.__unicode__()
	        retorno.append({'pk':ed.pk, 'valor':descricao})

        if not retorno:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    else:
        raise Http404
    return HttpResponse(json, mimetype="application/json")

def escolhe_patrimonio(request):
    if request.method == 'POST':
        num_doc = request.POST.get('num_doc')

        retorno = [{'pk':p.pk, 'valor':p.__unicode__()} for p in Patrimonio.objects.filter(Q(pagamento__protocolo__num_documento__icontains=num_doc)|Q(ns__icontains=num_doc))] or [{"pk":"0","valor":"Nenhum registro"}]
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
            for p in Patrimonio.objects.filter(patrimonio__isnull=True):
                ht = p.historico_atual
                if ht and ht.estado == estado:
                    no_estado.append(ht.id)

            no_estado = HistoricoLocal.objects.filter(id__in=no_estado)
            #entidades_ids = no_estado.values_list('endereco__endereco__entidade', flat=True).distinct()
            entidades_ids = []
            for h in no_estado:
                try:
                    entidades_ids.append(h.endereco.end.entidade.id)
                except:
		    pass
            entidades = []
            for e in Entidade.objects.filter(id__in=entidades_ids):
                detalhes = []
                #detalhes_ids = no_estado.values_list('endereco', flat=True).filter(endereco__endereco__entidade=e)
                detalhes_ids = [h.endereco.id for h in no_estado if h.endereco.end.entidade==e]
                for d in EnderecoDetalhe.objects.filter(id__in=detalhes_ids):
                    detalhes.append({'detalhe':d, 'patrimonio':Patrimonio.objects.filter(historicolocal__in=no_estado.filter(endereco=d))})
                entidades.append({'entidade':e, 'detalhes':detalhes})
            return TemplateResponse(request, 'patrimonio/por_estado.html', {'estado':estado, 'entidades':entidades})
    else:
        return TemplateResponse(request, 'patrimonio/sel_estado.html', {'estados':Estado.objects.all()})

@login_required
def por_tipo(request, pdf=0):
    if request.method == 'GET' and request.GET.get('tipo'):
        tipo_id = request.GET.get('tipo')
        tipo = get_object_or_404(Tipo, pk=tipo_id)
        return TemplateResponse(request, 'patrimonio/por_tipo.html', {'tipo':tipo, 'patrimonios':Patrimonio.objects.filter(tipo=tipo)})
    else:
        return TemplateResponse(request, 'patrimonio/sel_tipo.html', {'tipos':Tipo.objects.all()})

@login_required
def por_marca(request, pdf=0):
    if request.method == 'GET' and request.GET.get('marca'):
        marca = request.GET.get('marca')
        if pdf:
	    return render_to_pdf('patrimonio/por_marca.pdf', {'marca':marca, 'patrimonios':Patrimonio.objects.filter(marca=marca), 'filename':'inventario_por_marca.pdf'})
        return TemplateResponse(request, 'patrimonio/por_marca.html', {'marca':marca, 'patrimonios':Patrimonio.objects.filter(marca=marca)})
    else:
        return TemplateResponse(request, 'patrimonio/sel_marca.html', {'marcas':Patrimonio.objects.values_list('marca', flat=True).order_by('marca').distinct()})

@login_required
def por_local(request, pdf=0):
    if request.GET.get('endereco') is not None:
        atuais = []
        for p in Patrimonio.objects.filter(patrimonio__isnull=True):
            ht = p.historico_atual
            if ht:
                 atuais.append(ht.id)

        detalhe_id = request.GET.get('detalhe2')
        if not detalhe_id:
           detalhe_id = request.GET.get('detalhe1')
        if not detalhe_id:
           detalhe_id = request.GET.get('detalhe')
        if detalhe_id:
            detalhe = get_object_or_404(EnderecoDetalhe, pk=detalhe_id)
            detalhes = [detalhe]
            i = 0
            while i < len(detalhes):
                for ed in detalhes[i].enderecodetalhe_set.all():
                    detalhes.append(ed)
                i += 1
            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__in=detalhes)
            context = {'detalhe':detalhe, 'det':detalhe_id, 'detalhes':[{'patrimonio':Patrimonio.objects.filter(historicolocal__in=historicos).order_by('descricao', 'complemento')}]}
        else:
            endereco_id = request.GET.get('endereco')
            endereco = get_object_or_404(Endereco, pk=endereco_id)

            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__endereco=endereco)
            detalhes = []
            detalhes_ids = historicos.values_list('endereco', flat=True).filter(endereco__endereco=endereco)
            for d in EnderecoDetalhe.objects.filter(id__in=detalhes_ids):
                detalhes.append({'detalhe':d, 'patrimonio':Patrimonio.objects.filter(historicolocal__in=historicos.filter(endereco=d)).order_by('descricao', 'complemento')})
            context = {'endereco':endereco, 'end':endereco_id, 'detalhes':detalhes}

        if pdf:
            return render_to_pdf('patrimonio/por_local.pdf', context, filename='inventario_por_local.pdf')
        return render_to_response('patrimonio/por_local.html', context)
    else:
        return render_to_response('patrimonio/sel_local.html', {'entidades':Entidade.objects.filter(entidade__isnull=True)}, context_instance=RequestContext(request))

@login_required
def por_tipo_equipamento(request, pdf=0):
    if request.method != 'GET':
        raise Http404

    if len(request.GET) < 1:
        return TemplateResponse(request, 'patrimonio/sel_tipo_equip.html', {'tipos':TipoEquipamento.objects.all(), 'estados':Estado.objects.all(), 'pns':Equipamento.objects.values_list('part_number', flat=True).order_by('part_number').distinct()})

    tipo_id = request.GET.get('tipo')
    entidades = []
    if tipo_id == '0':
        patrimonios_tipo = Patrimonio.objects.all()
        tipo = 'todos'
    else:
        patrimonios_tipo = Patrimonio.objects.filter(equipamento__tipo__id=tipo_id)
        tipo = TipoEquipamento.objects.get(id=tipo_id)

    estado_id = request.GET.get('estado')
    if estado_id != '0':
        for p in patrimonios_tipo:
            if p.historico_atual is None:
                patrimonios_tipo = patrimonios_tipo.exclude(id=p.id)
            elif p.historico_atual.estado.id != int(estado_id):
                patrimonios_tipo = patrimonios_tipo.exclude(id=p.id)

    part_number = request.GET.get('partnumber')
    if part_number != '0':
        patrimonios_tipo = patrimonios_tipo.filter(equipamento__part_number=part_number)

    for p in patrimonios_tipo:
        if p.historico_atual:
            entidades.append({'entidade':p.historico_atual.endereco.end.entidade, 'local':p.historico_atual.endereco.complemento, 'patrimonio':p})

    entidades.sort(key=lambda x: x['local'])
    entidades.sort(key=lambda x: x['entidade'].sigla)

    entidade = ''
    local = ''
    for i in range(len(entidades)):
        if entidades[i]['entidade'] != entidade:
            entidade = entidades[i]['entidade']
            local = entidades[i]['local']
            continue
        if entidades[i]['local'] != local:
            local = entidades[i]['local']
            entidades[i]['entidade'] = ''
            continue

        entidades[i]['entidade'] = ''
        entidades[i]['local'] = ''

    return TemplateResponse(request, 'patrimonio/por_tipo_equipamento.html', {'entidades':entidades, 'tipo':tipo})

@login_required
def por_tipo_equipamento_old(request, pdf=0):
    if request.method != 'GET':
        raise Http404

    if len(request.GET) < 1:
        return TemplateResponse(request, 'patrimonio/sel_tipo_equip.html', {'tipos':TipoEquipamento.objects.all(), 'estados':Estado.objects.all(), 'pns':Equipamento.objects.values_list('part_number', flat=True).order_by('part_number').distinct()})

    tipo_id = request.GET.get('tipo')
    entidades = []
    if tipo_id == '0':
        patrimonios_tipo = Patrimonio.objects.all()
        tipo = 'todos'
    else:
        patrimonios_tipo = Patrimonio.objects.filter(equipamento__tipo__id=tipo_id)
        tipo = TipoEquipamento.objects.get(id=tipo_id)

    estado_id = request.GET.get('estado')
    if estado_id != '0':
        for p in patrimonios_tipo:
            if p.historico_atual is None:
                patrimonios_tipo = patrimonios_tipo.exclude(id=p.id)
            elif p.historico_atual.estado.id != int(estado_id):
                patrimonios_tipo = patrimonios_tipo.exclude(id=p.id)

    part_number = request.GET.get('partnumber')
    if part_number != '0':
	patrimonios_tipo = patrimonios_tipo.filter(equipamento__part_number=part_number)

    for e in Entidade.objects.all():
        patrimonios_entidade = patrimonios_tipo.all()

        for p in patrimonios_entidade:
            if p.historico_atual is None:
                patrimonios_entidade = patrimonios_entidade.exclude(id=p.id)
            elif p.historico_atual.endereco.end.entidade != e:
                patrimonios_entidade = patrimonios_entidade.exclude(id=p.id)
        if patrimonios_entidade.count() > 0:
            entidade = {'entidade':e}
            locais = []
            for l in sorted(set([p.historico_atual.endereco.complemento for p in patrimonios_entidade])):
                patrimonios_local = patrimonios_entidade.all()
                for p in patrimonios_local:
                    if p.historico_atual is None:
                        patrimonios_local = patrimonios_local.exclude(id=p.id)
                    elif p.historico_atual.endereco.complemento != l:
			patrimonios_local = patrimonios_local.exclude(id=p.id)
                local={'local':l, 'patrimonios':patrimonios_local}
	        locais.append(local)
            entidade['locais'] = locais
            entidades.append(entidade)
    
    return TemplateResponse(request, 'patrimonio/por_tipo_equipamento.html', {'entidades':entidades, 'tipo':tipo})

@login_required
def filtra_pn_estado(request):
    tipo_id = request.POST.get('id')
    if tipo_id == '0':
        part_numbers = Equipamento.objects.values_list('part_number', flat=True).order_by('part_number').distinct()
        patrimonios = Patrimonio.objects.all()
    else:
        part_numbers = Equipamento.objects.filter(tipo__id=tipo_id).values_list('part_number', flat=True).order_by('part_number').distinct()
        patrimonios = Patrimonio.objects.filter(equipamento__tipo__id=tipo_id)

    pns = []
    for p in part_numbers:
        pns.append({'pk':p, 'value':'%s (%s)' % (p, patrimonios.filter(equipamento__part_number=p).order_by('id').distinct().count())})

    estados = []
    for e in Estado.objects.all():
        patrimonios_estado = patrimonios.all()
        for p in patrimonios_estado:
            if not p.historico_atual:
                patrimonios_estado = patrimonios_estado.exclude(id=p.id)
            elif p.historico_atual.estado !=e:
		patrimonios_estado = patrimonios_estado.exclude(id=p.id)

        estados.append({'pk':e.id, 'value':'%s (%s)' % (e, patrimonios_estado.order_by('id').distinct().count())})

    retorno = {'estados':estados, 'pns':pns}
    json = simplejson.dumps(retorno)

    return HttpResponse(json, mimetype="application/json")

@login_required
def por_termo(request, pdf=0):
    termo_id = request.GET.get('termo')
    modalidade = request.GET.get('modalidade')
    agilis = request.GET.get('agilis')
    doado = request.GET.get('doado')
    localizado = request.GET.get('localizado')
    numero_fmusp = request.GET.get('numero_fmusp')
    template_name = 'por_termo'

    if termo_id is None:
        return TemplateResponse(request, 'patrimonio/escolhe_termo.html', {'termos':Termo.objects.all()})

    if termo_id != '0':
        qs = Termo.objects.filter(id=termo_id)
    else:
        qs = Termo.objects.exclude(id=9)

    termos = []

    if agilis == '0':
        patrimonios = Patrimonio.objects.filter(agilis=False)
    elif agilis == '1':
        patrimonios = Patrimonio.objects.filter(agilis=True)
    else:
        patrimonios = Patrimonio.objects.all()

    if doado == '0':
        patrimonios = patrimonios.exclude(historicolocal__endereco__id=1372, historicolocal__estado__id=1)
    elif doado == '1':
	patrimonios = patrimonios.filter(historicolocal__endereco__id=1372, historicolocal__estado__id=1)

    if localizado == '1':
	patrimonios = patrimonios.exclude(historicolocal__endereco__complemento__icontains='Localizado')
    elif localizado == '0':
        patrimonios = patrimonios.filter(historicolocal__endereco__complemento__icontains='Localizado')

    if modalidade == '1':
        patrimonios = patrimonios.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla__in=['MPN', 'MPI'])
    elif modalidade == '2':
        patrimonios = patrimonios.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla__in=['MCN', 'MCI'])

    if numero_fmusp == '1':
	patrimonios = patrimonios.filter(numero_fmusp__isnull=False)
        template_name = 'por_termo_fm'

    for t in qs:
        termo = {'termo':t}
        tps = []
        pat_termo = patrimonios.filter(pagamento__protocolo__termo=t)
        if numero_fmusp == '1':
            termo.update({'patrimonios':pat_termo.order_by('numero_fmusp', 'descricao', 'complemento')})
            termos.append(termo)
            continue

        tipos = pat_termo.values_list('tipo', flat=True).order_by('tipo').distinct()
        for tipo in Tipo.objects.filter(id__in=tipos):
            tp = {'tipo':tipo}
            pgtos = []
            pt = pat_termo.filter(tipo=tipo)
            pagtos = pt.values_list('pagamento', flat=True).order_by('numero_fmusp').distinct()
            for pg in Pagamento.objects.filter(id__in=pagtos):
                pgto = {'pg': pg, 'patrimonios':pt.filter(pagamento=pg).order_by('numero_fmusp', 'descricao', 'complemento')}
                pgtos.append(pgto)
            tp.update({'pagamentos':pgtos})
            tps.append(tp)
        termo.update({'tipos':tps})
        termos.append(termo)

    if pdf:
        vars = {'termos':termos, 'i':itertools.count(1), 'numero_fmusp':numero_fmusp}
        if termo_id !=0 and len(qs) > 0:
            vars.update({'t':qs[0]})
	return render_to_pdf('patrimonio/%s.pdf' % template_name, vars, filename='invertario_por_termo.pdf')
    else:
        return TemplateResponse(request, 'patrimonio/%s.html' % template_name, {'termos':termos, 'i':itertools.count(1), 't':qs[0], 'm':modalidade, 'a':agilis, 'd':doado, 'l':localizado, 'numero_fmusp':numero_fmusp})

@login_required
def racks(request):
        
    # Busca patrimonios do tipo RACK com o estado ATIVO
    locais = Patrimonio.objects.filter(equipamento__tipo__nome='Rack', historicolocal__estado__id=Estado.PATRIMONIO_ATIVO).values_list('historicolocal__endereco', flat=True).order_by('historicolocal__endereco').distinct().only('id')

    todos_dcs = []
    for local in locais:
        dc = {'nome':EnderecoDetalhe.objects.get(id=local).complemento, 'id':local}
        todos_dcs.append(dc)

    p_dc = request.GET.get('dc')
    
    dcs = []
    if p_dc != None:
        if int(p_dc) > 0:
            locais = locais.filter(historicolocal__endereco__id=p_dc)
        
        for local in locais:
            racks = []
            patrimonio_racks = Patrimonio.objects.filter(equipamento__tipo__nome='Rack', historicolocal__endereco__id=local).select_related('equipamento', 'equipamento__imagem', 'historicolocal', 'contido')
            for rack in patrimonio_racks:
                altura = 127
                vazio = 0
                equipamentos = []
                conflitos = []
                
                eixoY = 0
                
                # ordena os equipamentos do rack conforme a posição no rack
#                 pts = list(rack.contido.filter(historicolocal__posicao__isnull=False).values('historicolocal__data').aggregate(Max('historicolocal__data')))
                hist = rack.contido.annotate(hist=Max('historicolocal__data')).values_list('pk')
                pts = list(rack.contido.filter(pk__in=hist))
                pts.sort(key=lambda x: x.historico_atual.posicao_int, reverse=True)
    
                ptAnterior = None
                for pt in pts:
                    pos = pt.historico_atual.posicao_int -1 
    
                    if pos <= 0 or pt.tamanho is None: continue
                    
                    # calculando a altura do pt
                    if altura > pos+int(round(pt.tamanho*3)):
                        tam = altura-(pos+int(round(pt.tamanho*3)))
                        altura -= tam
                        #equipamentos.append({'tamanho':tam, 'range':range(tam-1)})
                        vazio += tam
                    tam = int(round(pt.tamanho*3))
                    altura -= tam
                    
                    # Setando Imagem do equipamento
                    imagem = None
                    if pt.equipamento and pt.equipamento.imagem:
                        imagem = pt.equipamento.imagem.url
    
                    # calculo da posição em pixel do eixoY, top-down
                    eixoY = int(round(((126 - (pos) - tam) * 19)/3))
                    
                    # x a partir do topo do container
                    equipamentos.append({'id': pt.id, 'pos':pos, 'tam': tam, 'eixoY': eixoY, 'altura':(tam*19/3), 'pos_original':pt.historico_atual.posicao_int, 'imagem':imagem, 'descricao':pt.descricao or u'Sem descrição', 'range':range(tam-1), 'conflito':False})
                    
                    if pos + (tam) > 126:
                        # Ocorre quando um equipamento está passando do limite máximo do rack
                        #obs = '{!s} + {!s} > {!s}'.format(pos, (tam), 126)
                        obs = '%s + %s > %s' % (pos, tam, 125)
                        conflitos.append({'obs': obs, 'eq1':equipamentos[-1]})
                        equipamentos[-1]['conflito'] = True
                
                    elif len(equipamentos)>2 and eixoY:
                        # Ocorre quando um equipamento sobrepoe o outro
                        if ptAnterior['eixoY'] + ptAnterior['tam'] > eixoY:
                            #obs = '{!s} + {!s} > {!s}'.format(ptAnterior['eixoY'], ptAnterior['tam'], eixoY)
                            obs = '%s + %s > %s' % (ptAnterior['eixoY'], ptAnterior['tam'], eixoY)
                            conflitos.append({'obs': obs, 'eq1':ptAnterior, 'eq2':equipamentos[-1]})
                            equipamentos[-1]['conflito'] = True
                            equipamentos[-2]['conflito'] = True
                    elif pos < 0:
                        # Posição negativa
                        # Ocorre quando o equipamento não tem uma posição válida
                        #obs = '{!s} < 0'.format(pt.historico_atual().posicao_int())
                        obs = '%s < 0' % pt.historico_atual.posicao_int()
                        conflitos.append({'obs': obs, 'eq1':equipamentos[-1]})
                        equipamentos[-1]['conflito'] = True
    
                    ptAnterior = equipamentos[-1]
                
                rack = {'id':rack.id, 'nome':rack.apelido, 'altura':126, 'altura_pts': 126/3, 'equipamentos':equipamentos, 'conflitos':conflitos}
                
                # Calculo de uso do rack
                if altura > 1:
                    equipamentos.append({'tam':altura-1, 'range':range(altura-2)})
                    vazio += altura-1
                    
                rack['vazio'] = '%.2f%%'    % ((rack['altura']-vazio)*100.0/rack['altura'],)
                racks.append(rack)
                
            dc = {'nome':EnderecoDetalhe.objects.get(id=local).complemento, 'racks':racks, 'id':local}
            dcs.append(dc)
            
    return TemplateResponse(request, 'patrimonio/racks.html', {'dcs':dcs, 'todos_dcs':todos_dcs})

@login_required
def racks1(request):
    detalhes = [ed for ed in EnderecoDetalhe.objects.filter(complemento__contains='.F', tipo__nome__startswith='Posi').order_by('-complemento') if len(ed.complemento.split('.'))==2 and ed.end.id==60]
    racks = []
    r = ''
    rack = ''
    alt = 0
    vazio = 0
    for ed in detalhes:
        equipamentos = []
        info = ed.complemento.split('.')
        if info[0] != r:
            if alt > 1: 
                equipamentos.append({'tamanho':alt-1, 'range':range(alt-2)})
		vazio += alt-1
            r = info[0]
            if rack:
                rack['vazio'] = '%.2f%%' % ((rack['altura']-vazio)*100.0/rack['altura'],)
                racks.append(rack)
            equipamentos = []
            rack = {'nome':r, 'altura':126, 'equipamentos':equipamentos}
            alt=127
            vazio = 0
        hl = HistoricoLocal.objects.filter(endereco=ed, patrimonio__patrimonio__isnull=True)
        if hl.count() > 0:
            pt = hl[0].patrimonio
            try:
                pos = int(info[1][1:])
            except: continue
            if pos == 1 or pt.tamanho is None: continue
            if alt > pos+int(round(pt.tamanho*3)):
                tam = alt-(pos+int(round(pt.tamanho*3)))
                alt -= tam
                equipamentos.append({'tamanho':tam, 'range':range(tam-1)})
                vazio += tam
            tam = int(round(pt.tamanho*3))
            alt -= tam
            imagem = None
            if pt.equipamento:
                if pt.equipamento.imagem:
		    imagem = pt.equipamento.imagem.url
            equipamentos.append({'tamanho':tam, 'imagem':imagem, 'descricao':pt.descricao or u'Sem descrição', 'range':range(tam-1)})

    return TemplateResponse(request, 'patrimonio/racks.html', {'racks':racks})
    #return render_to_pdf('patrimonio/racks.pdf', {'racks':racks})


@login_required
def presta_contas(request):
    termos = []
    for t in Termo.objects.all():
        termo = {'termo':t}
        termos.append(termo)

    return TemplateResponse(request, 'patrimonio/presta_contas.html', {'termos':termos})

@login_required
def abre_arvore(request):
    ret = []
    if request.GET.get('id'):
        id = request.GET.get('id')
        model = request.GET.get('model')
        if model == 'termo':
	    for n in Termo.objects.get(id=id).natureza_gasto_set.filter(item__origemfapesp__pagamento__patrimonio__isnull=False).distinct():
	        ret.append({'data':n.modalidade.sigla, 'attr':{'style':'padding-top:4px;', 'o_id':n.id, 'o_model': n._meta.module_name}})
        elif model == 'natureza_gasto':
            for i in Natureza_gasto.objects.get(id=id).item_set.filter(origemfapesp__pagamento__patrimonio__isnull=False).distinct():
                ret.append({'data':i.__unicode__(), 'attr':{'style':'padding-top:4px;', 'o_id':i.id, 'o_model': i._meta.module_name}})
        elif model == 'item':
	    for o in Item.objects.get(id=id).origemfapesp_set.filter(pagamento__patrimonio__isnull=False).distinct():
                for p in o.pagamento_set.filter(patrimonio__isnull=False).distinct():
                    ret.append({'data':'%s %s' % (p.protocolo.tipo_documento.sigla or '', p.protocolo.num_documento), 'attr':{'style':'padding-top:4px;', 'o_id':p.id, 'o_model':p._meta.module_name}})
        elif model == 'pagamento':
            for pt in Pagamento.objects.get(id=id).patrimonio_set.all():
                ret.append({'data':'<div><div class="col1"></div><div class="col2"><div class="menor">%s</div><div class="maior">%s</div><div class="maior">%s - %s</div><div class="medio">%s</div><div class="menor">%s</div><div class="menor">%s</div><div class="menor">%s</div></div><div style="clear:both;"></div></div>' % (pt.tipo, pt.ns, pt.descricao, pt.complemento, pt.equipamento.tipo, pt.valor, 'Sim' if pt.agilis else u'Não', 'Sim' if pt.checado else u'Não'), 'attr':{'style':'height:130px;'}})
    else:
        for t in Termo.objects.all():
	    ret.append({'data':t.__unicode__(), 'attr':{'style':'padding-top:6px;', 'o_id':t.id, 'o_model': t._meta.module_name}})
    json = simplejson.dumps(ret)
    return HttpResponse(json, mimetype="application/json")


@login_required
def por_tipo_equipamento2(request):
    return TemplateResponse(request, 'patrimonio/por_tipo_equipamento2.html')


@login_required
def abre_arvore_tipo(request):
    ret = []
    if request.GET.get('id'):
        id = request.GET.get('id')
        model = request.GET.get('model')
        if model == 'tipoequipamento':
            for e in TipoEquipamento.objects.get(id=id).equipamento_set.all():
		ret.append({'data':e.descricao, 'attr':{'style':'padding-top:4px;', 'o_id':e.id, 'o_model': e._meta.module_name}})
        elif model == 'equipamento':
            patrimonios = list(Equipamento.objects.get(id=id).patrimonio_set.all())
            try:
                patrimonios.sort(key=lambda x:x.historico_atual.endereco.end.entidade.sigla)
            except:
		pass
            for p in patrimonios:
                ha = p.historico_atual
		ret.append({'data':'<div><div class="col1"></div><div class="col2"><div class="medio">%s</div><div class="maior">%s</div><div class="menor">%s</div><div class="medio">%s</div><div class="medio">%s</div><div class="medio">%s</div><div class="medio">%s</div><div class="menor">%s</div></div><div style="clear:both;"></div></div>' % (ha.endereco.end.entidade if ha else 'ND' , ha.endereco.complemento if ha else 'ND', ha.posicao if ha and ha.posicao else 'ND', p.equipamento.marca, p.equipamento.modelo, p.equipamento.part_number, p.ns, ha.estado if ha else 'ND'), 'attr':{'style':'padding-top:4px;'}})
    else:
        for tp in TipoEquipamento.objects.all():
            #ret.append({'data':'%s <a onclick="$(\'#blocos\').jstree(\'open_all\', \'#%s-%s\')" style="color:#0000aa;">Abrir tudo</a>' % (tp.__unicode__(), tp._meta.module_name, tp.id), 'attr':{'id':'%s-%s'% (tp._meta.module_name, tp.id), 'style':'padding-top:6px;', 'o_id':tp.id, 'o_model': tp._meta.module_name}})
            ret.append({'data':'%s <a onclick="abre_fecha(\'%s-%s\', \'blocos\')" id="a-%s-%s" style="color:#0000aa;">Abrir tudo</a>' % (tp.__unicode__(), tp._meta.module_name, tp.id, tp._meta.module_name, tp.id), 'attr':{'id':'%s-%s'% (tp._meta.module_name, tp.id), 'style':'padding-top:6px;', 'o_id':tp.id, 'o_model': tp._meta.module_name}})



    json = simplejson.dumps(ret)
    return HttpResponse(json, mimetype="application/json")
