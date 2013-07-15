# -*- coding: utf-8 -*-

# Create your views here.

import datetime
from models import *
from utils.functions import render_to_pdf
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import messages
from forms import *
from django.core.urlresolvers import reverse

def ferias(context):
    now = datetime.datetime.now()
    funcionarios = []
    for f in [m for m in Membro.objects.all() if m.funcionario is True]:
        func = {}
        func['nome'] = f.nome
        h = Historico.ativos.get(funcionario=True, membro=f)
        func['admissao'] = h.inicio.strftime("%d/%m/%Y")
        ferias = f.ferias_set.order_by('-inicio')
        if ferias.count() == 0:
            continue
        ferias = ferias[0]
        final = ferias.inicio - datetime.timedelta(1)
        final = datetime.date(final.year+1, final.month, final.day)
        func['periodo'] = '%s a %s' % (ferias.inicio.strftime("%d/%m/%Y"), final.strftime("%d/%m/%Y"))
        try:
            cf = ferias.controleferias_set.get(oficial=True)
        except:
            continue
        func['ferias'] = '%s a %s' % (cf.inicio.strftime("%d/%m/%Y"), cf.termino.strftime("%d/%m/%Y"))
        dias = cf.termino - cf.inicio
        func['dias'] = dias.days + 1
        func['decimo_terceiro'] = u'Sim' if ferias.decimo_terceiro else u'Não'

        funcionarios.append(func)

    return render_to_pdf('membro/ferias.pdf', {'funcionarios':funcionarios, 'ano':now.year+1})

@login_required
def controle(request):
    user = request.user
    membro = get_object_or_404(Membro, contato__email=user.email)

    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == u'entrada':
            controle = Controle()
            controle.membro = membro
            controle.entrada = datetime.datetime.now()
        else:
            controle = membro.controle_set.all()[0]
            controle.saida = datetime.datetime.now()
        controle.save()
        messages.info(request, u'Sua %s foi registrada com sucesso.' % acao)
        return HttpResponseRedirect(reverse('membro.views.observacao', kwargs={'id':controle.id}))

    raise Http404


@login_required
def mensal(request, ano=2012, mes=7):
    membro_ids = Controle.objects.filter(entrada__year=ano, entrada__month=mes).order_by('membro').values_list('membro', flat=True).distinct()
    membros = Membro.objects.filter(id__in=membro_ids)
    from calendar import monthrange
    last_day = monthrange(int(ano), int(mes))[1]
    dias = range(1,last_day+1)
    dados = []
    for m in membros:
        linha = [m.nome]
        controles = Controle.objects.filter(entrada__year=ano, entrada__month=mes, membro=m, saida__isnull=False)
        for dia in dias:
            min = sum([c.segundos() for c in controles.filter(entrada__day=dia)], 0)/60
            linha.append('%02d:%02d' % (min/60, min%60))
        dados.append(linha)

    return TemplateResponse(request, 'membro/mensal.html', {'dados':dados, 'dias':dias, 'ano':ano, 'mes':mes})

@login_required
def detalhes(request):
    membro = get_object_or_404(Membro, contato__email=request.user.email)
    agora = datetime.datetime.now()

    return TemplateResponse(request, 'membro/detalhes.html', {'membro':membro, 'dados':Controle.objects.filter(membro=membro, entrada__month=agora.month)})

@login_required
def mensal_func(request):
    if request.GET.get('ano'):
        meses = []
        funcionario = request.GET.get('funcionario')
        membro = Membro.objects.get(id=funcionario)
	if request.user.is_superuser == False and  request.user.email != membro.email: 
	    raise Http404
        ano = request.GET.get('ano')
        mes = request.GET.get('mes')
        controles = Controle.objects.filter(membro=funcionario)
        if ano > '0': controles = controles.filter(entrada__year=ano)
        if mes > '0': controles = controles.filter(entrada__month=mes)
 
        mes = 'acb'
        if controles.count() > 0:
            for c in controles:
                m = c.entrada.strftime('%m/%Y')
                if m != mes:
                    cm = [c]
                    mes = m
                    meses.append({'mes':mes, 'controles':cm})
                else:
		    cm.append(c)

        for m in meses:
	    total = sum([c.segundos() for c in m['controles']])
            total = '%2dh%2dmin' % (total/3600, total/60%60)
            m.update({'total':total})
        return TemplateResponse(request, 'membro/detalhe.html', {'meses':meses, 'membro':membro})
    else:
        hoje = datetime.datetime.now()
        anos = [0]+range(2012, hoje.year+1)
        meses = range(13)
        funcionarios = [m for m in Membro.objects.all() if m.funcionario]

        return TemplateResponse(request, 'membro/sel_func.html', {'anos':anos, 'meses':meses, 'funcionarios':funcionarios})

@login_required
def observacao(request, id):
    controle = get_object_or_404(Controle, pk=id)

    if request.user.email != controle.membro.email:
        return HttpResponseForbidden()

    if request.method == 'POST':
        if request.POST.get('enviar'):
            f = ControleObs(request.POST, instance=controle)
            f.save()

        return HttpResponseRedirect('/')
    else:
        f = ControleObs(instance=controle)
        return TemplateResponse(request, 'membro/observacao.html', {'form':f})

