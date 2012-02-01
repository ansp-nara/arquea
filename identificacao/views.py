# -*- coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from models import *
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def escolhe_entidade(request):
    if request.method == 'POST':
        ent_id = request.POST.get('entidade')
	entidade = get_object_or_404(Entidade, pk=ent_id)

	retorno = []
	for ed in Endereco.objects.filter(entidade=entidade):
	    descricao = '%s' % (ed.__unicode__())
	    retorno.append({'pk':ed.pk, 'valor':descricao})

        if not retorno:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    else:
        raise Http404
    return HttpResponse(json, mimetype="application/json")

def escolhe_endereco(request):
    if request.method == 'POST':
        end_id = request.POST.get('endereco')
        endereco = get_object_or_404(Endereco, pk=end_id)

        retorno = []
        for d in endereco.enderecodetalhe_set.all():
            descricao = '%s' % (d.__unicode__())
            retorno.append({'pk':d.pk, 'valor':descricao})

        if not retorno:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]

        json = simplejson.dumps(retorno)
    else:
        raise Http404
    return HttpResponse(json, mimetype="application/json")

@login_required
def arquivos_entidade(request):
    return render_to_response('identificacao/arquivos_entidade.html', {'entidades': [e for e in Entidade.objects.all() if e.arquivoentidade_set.count() > 0]}, context_instance=RequestContext(request))
