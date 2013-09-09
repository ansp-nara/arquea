# -*- coding: utf-8 -*-

# Create your views here.

from datetime import date, timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from forms import *
from models import *
from protocolo.models import Feriado
from utils.functions import render_to_pdf
import calendar
import logging
import json as simplejson

# Get an instance of a logger
logger = logging.getLogger(__name__)

def ferias(context):
    now = datetime.now()
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
        final = ferias.inicio - timedelta(1)
        final = date(final.year+1, final.month, final.day)
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
            controle.entrada = datetime.now()
        else:
            controle = membro.controle_set.all()[0]
            controle.saida = datetime.now()
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
    agora = datetime.now()

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
        
        c = Controle.objects.filter(membro=funcionario)[:1].get()

        # Contagem de total geral do funcionario
        total_meses = c.total_analitico_horas(0, 0)
        total_geral_banco_horas = 0
        for m in total_meses:
             # soma horas extras somente dos meses que não forem o mês em andamento
             total_geral_banco_horas += m['total_banco_horas']
              
        if total_geral_banco_horas >= 0:
            total_geral_banco_horas_str = '%2dh %02dmin' % (total_geral_banco_horas/3600, total_geral_banco_horas/60%60)
        else:
            total_geral_banco_horas_str = '-%2dh %02dmin' % (-total_geral_banco_horas/3600, -total_geral_banco_horas/60%60)
        total_geral_ferias = Ferias().total_dias_uteis_aberto(funcionario)
        total_geral_ferias_str = '%2dh %02dmin' % (total_geral_ferias/3600, total_geral_ferias/60%60)
#         
        meses = c.total_analitico_horas(ano, mes)
        
        total_banco_horas = 0
        total_horas = 0
        total_horas_periodo = 0
        total_horas_restante = 0
        total_horas_dispensa = 0
        total_horas_ferias = 0
         
        for m in meses:
                        
            # total de horas trabalhadas
            total_horas += m['total']
            total_str = '%2dh %02dmin' % (m['total']/3600, m['total']/60%60)
            m.update({'total':total_str})
             
            # as horas totais do período são as horas do total de dias do mes menos os finais de semana, ferias e dispensas
            total_horas_periodo += m['total_horas_periodo']
            total_horas_periodo_str = '%2dh %02dmin' % (m['total_horas_periodo']/3600, m['total_horas_periodo']/60%60)
            m.update({'total_horas_periodo':total_horas_periodo_str})
             
            total_horas_restante += m['total_horas_restante']
            if m['total_horas_restante'] >= 0:
                total_horas_restante_str = '%02dh %02dmin' % (m['total_horas_restante']/3600.0, m['total_horas_restante']/60%60)
            else:
                total_horas_restante_str = '-%02dh %02dmin' % (-m['total_horas_restante']/3600.0, -m['total_horas_restante']/60%60)
            m.update({'total_horas_restante':total_horas_restante_str})
            
            total_horas_ferias += m['total_horas_ferias']
            total_horas_ferias_str = '%2dh %02dmin' % (m['total_horas_ferias']/3600, m['total_horas_ferias']/60%60)
            m.update({'total_horas_ferias':total_horas_ferias_str})
            
            total_horas_dispensa += m['total_horas_dispensa']
            total_horas_dispensa_str = '%2dh %02dmin' % (m['total_horas_dispensa']/3600, m['total_horas_dispensa']/60%60)
            m.update({'total_horas_dispensa':total_horas_dispensa_str})
            # soma horas extras somente dos meses que não forem o mês em andamento
            total_banco_horas += m['total_banco_horas']
            if m['total_banco_horas'] >= 0:
                total_banco_horas_str = '%2dh %02dmin' % (m['total_banco_horas']/3600, m['total_banco_horas']/60%60)
            else:
                total_banco_horas_str = '-%2dh %02dmin' % (-m['total_banco_horas']/3600, -m['total_banco_horas']/60%60)
            m.update({'total_banco_horas':total_banco_horas_str})
            
        
        if total_horas_restante >= 0:
             total_horas_restante_str = '%2dh %02dmin' % (total_horas_restante/3600, total_horas_restante/60%60)
        else:
             total_horas_restante_str = '-%2dh %02dmin' % (-total_horas_restante/3600, -total_horas_restante/60%60)
             
        if total_banco_horas >= 0:
             total_banco_horas_str = '%2dh %02dmin' % (total_banco_horas/3600, total_banco_horas/60%60)
        else:
             total_banco_horas_str = '-%2dh %02dmin' % (-total_banco_horas/3600, -total_banco_horas/60%60)
        
        
        total_horas_str = '%2dh %02dmin' % (total_horas/3600, total_horas/60%60)
        total_horas_periodo_str = '%2dh %02dmin' % (total_horas_periodo/3600, total_horas_periodo/60%60)
        total_horas_dispensa_str = '%2dh %02dmin' % (total_horas_dispensa/3600, total_horas_dispensa/60%60)
        total_horas_ferias_str = '%2dh %02dmin' % (total_horas_ferias/3600, total_horas_ferias/60%60)
        
        return TemplateResponse(request, 'membro/detalhe.html', {'meses':meses, 'membro':membro, 'total_banco_horas':total_banco_horas_str,
                                'total_horas':total_horas_str, 'total_horas_periodo':total_horas_periodo_str,
                                'total_horas_restante':total_horas_restante_str, 'total_horas_dispensa':total_horas_dispensa_str,
                                'total_horas_ferias':total_horas_ferias_str,
                                'total_geral_banco_horas':total_geral_banco_horas_str, 'total_geral_ferias':total_geral_ferias_str})
    else:
        hoje = datetime.now()
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


@login_required
def controle_mudar_almoco(request):
    controle_id = request.GET.get('id')
    almoco = request.GET.get('almoco')
    
#     if request.user.is_superuser == False or not controle_id:
    if not controle_id: 
        raise Http404
    
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.almoco_devido = True
    controle.almoco = almoco
    controle.save()
    
    json = simplejson.dumps('ok')
    return HttpResponse(json, mimetype="application/json")


@login_required
def controle_avancar_bloco(request):
    controle_id = request.GET.get('id')
    tempo = request.GET.get('tempo')
    
#     if request.user.is_superuser == False or not controle_id:
    if not controle_id or not tempo: 
        raise Http404
    
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.entrada = controle.entrada + timedelta(minutes=int(tempo))
    controle.saida = controle.saida + timedelta(minutes=int(tempo)) 
    controle.save()
    
    json = simplejson.dumps('ok')
    return HttpResponse(json, mimetype="application/json")


@login_required
def controle_voltar_bloco(request):
    controle_id = request.GET.get('id')
    tempo = request.GET.get('tempo')
    
#     if request.user.is_superuser == False or not controle_id:
    if not controle_id or not tempo: 
        raise Http404
    
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.entrada = controle.entrada - timedelta(minutes=int(tempo))
    controle.saida = controle.saida - timedelta(minutes=int(tempo)) 
    controle.save()
    
    json = simplejson.dumps('ok')
    return HttpResponse(json, mimetype="application/json")


@login_required
def controle_adicionar_tempo_final(request):
    controle_id = request.GET.get('id')
    tempo = request.GET.get('tempo')
    
#     if request.user.is_superuser == False or not controle_id:
    if not controle_id or not tempo: 
        raise Http404
    
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.saida = controle.saida + timedelta(minutes=int(tempo)) 
    controle.save()
    
    json = simplejson.dumps('ok')
    return HttpResponse(json, mimetype="application/json")

@login_required
def controle_adicionar_tempo_inicial(request):
    controle_id = request.GET.get('id')
    tempo = request.GET.get('tempo')
    
#     if request.user.is_superuser == False or not controle_id:
    if not controle_id or not tempo: 
        raise Http404
    
    controle = get_object_or_404(Controle, pk=controle_id)
    controle.entrada = controle.entrada - timedelta(minutes=int(tempo)) 
    controle.save()
    
    json = simplejson.dumps('ok')
    return HttpResponse(json, mimetype="application/json")
