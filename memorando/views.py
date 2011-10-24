# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from financeiro.models import Pagamento
from outorga.models import Termo
from django.utils import simplejson
from django.http import Http404, HttpResponse
from utils.functions import render_to_pdf
from models import *
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.html import strip_tags

# Create your views here.

@login_required
def simples(request, mem):
    m = get_object_or_404(MemorandoSimples,pk=mem)

    return render_to_pdf('memorando/simples.pdf', {'m':m}, filename='memorando_%s.pdf' % m.__unicode__())

def escolhe_pagamentos(request):

    if request.method == 'POST':
        termo_id = request.POST.get('termo')
        termo = get_object_or_404(Termo, pk=termo_id)

	pagamentos = []

        for p in Pagamento.objects.filter(protocolo__termo=termo).order_by('protocolo__num_documento'):
            a = p.auditoria_set.all()
            if a.count():
                a = a[0]
                valor = u'%s - %s, parcial %s, página %s' % (p.protocolo.num_documento, p.valor_fapesp, a.parcial, a.pagina)
            else:
                valor = u'%s %s' % (p.protocolo.num_documento, p.valor_fapesp)

	    pagamentos.append({'pk':p.id, 'valor':valor})

        json = simplejson.dumps(pagamentos)

        return HttpResponse(json, mimetype="application/json")

def escolhe_pergunta(request):
    if request.method == 'POST':
        pergunta_id = request.POST.get('pergunta')
        pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
        json = simplejson.dumps(pergunta.questao)
        return HttpResponse(json, mimetype="application/json")

def filtra_perguntas(request):
    if request.method == 'POST':
        memorando_id = request.POST.get('memorando')
        memorando = get_object_or_404(MemorandoFAPESP, pk=memorando_id)
        
        perguntas = [{'pk':'', 'valor':'-----------'}]
        for p in memorando.pergunta_set.all():
            perguntas.append({'pk':p.id, 'valor':p.__unicode__()})

        return HttpResponse(simplejson.dumps(perguntas), mimetype="application/json")

@login_required
def fapesp(request, mem):
    m = get_object_or_404(MemorandoResposta,pk=mem)
    corpos = []
    incluidos = {}

    for c in m.corpo_set.all():
        if c.pergunta.numero in incluidos.keys():
            corpos[incluidos[c.pergunta.numero]]['respostas'].append(c.resposta)
        else:
            incluidos.update({c.pergunta.numero:len(corpos)})
            corpos.append({'numero':c.pergunta.numero, 'pergunta':c.pergunta.questao, 'respostas':[c.resposta]})

    return render_to_pdf('memorando/fapesp.pdf', {'m':m, 'corpos':corpos}, filename='memorando_%s.pdf' % m.data.strftime('%d_%m_%Y'))



@login_required
def relatorio(request):
    mem = request.GET.get('mem')
    if not mem:
        return render_to_response('memorando/escolhe_memorando.html', {'memorandos':MemorandoFAPESP.objects.all()})
    m = get_object_or_404(MemorandoFAPESP,pk=mem)
    return render_to_response('memorando/relatorio.html', {'memorando':m})

