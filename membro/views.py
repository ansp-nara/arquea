# -*- coding: utf-8 -*-

# Create your views here.

from datetime import date, timedelta, datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from forms import *
from models import *
from protocolo.models import Feriado
from utils.functions import render_to_pdf
import calendar
import logging

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

        total_horas_periodo = 0
        for m in meses:

            # total de horas trabalhadas	        
            total = sum([c.segundos() for c in m['controles']])
            total_str = '%2dh%2dmin' % (total/3600, total/60%60)
            m.update({'total':total_str})

            feriados = Feriado.objects.filter(feriado__year=c.entrada.year, feriado__month=c.entrada.month)
            
            folgas = DispensaLegal.objects.filter(membro=funcionario)
         
            # ferias_ini < mes_ini < ferias_fim  OR  mes_ini < ferias_ini < mes_fim
            mes_corrente_ini = date(c.entrada.year, c.entrada.month, 01)
            mes_corrente_fim = date(c.entrada.year, c.entrada.month, 01) + timedelta(calendar.monthrange(c.entrada.year, c.entrada.month)[1])
            ferias = ControleFerias.objects.filter(Q(inicio__lte=mes_corrente_ini, termino__gte=mes_corrente_ini) |
                                                   Q(inicio__gte=mes_corrente_ini, inicio__lte=mes_corrente_fim),
                                                   ferias__membro__id=funcionario)
            
            # int com o total de dias de trabalho (business day) no mes
            soma_dias_de_trabalho = 0
            # flag somente para a soma de dias durante o while. Sai quando trocar o mes
            date_flag = mes_corrente_ini
            while date_flag.month == c.entrada.month:
            
                # é final de semana?
                is_final_de_semana = date_flag.weekday() >= 5;
                
                # é feriado?
                is_feriado = False
                for feriado_dia in feriados:
                    is_feriado = is_feriado or (date_flag == feriado_dia.feriado)

                # é folga?
                is_folga = False
                for folga in folgas:
                    # gera um range de dias entre o período de início e final de folga
                    if folga.inicio_realizada == folga.termino_realizada:
                        is_folga = is_folga or (date_flag == folga.inicio_realizada)
                    else:
                        periodo_folga = (folga.inicio_realizada + timedelta(days=d) for d in range((folga.termino_realizada - folga.inicio_realizada).days + 1))
                        for dia_folga in periodo_folga:
                            is_folga = is_folga or (date_flag == dia_folga)

                # soma os dias de trabalho
                if not is_final_de_semana and not is_feriado and not is_folga:
                    soma_dias_de_trabalho = soma_dias_de_trabalho + 1
#                 else:
#                     logger.debug("nao e dia util =" + str(date_flag)
#                                  + (" is_final_de_semana=" + str(is_final_de_semana) if is_final_de_semana else "") 
#                                  + (" is_feriado=" + str(is_feriado) if is_feriado else "") 
#                                  + (" is_folga=" + str(is_folga) if is_folga else "")
#                     )
                
                date_flag = date_flag + timedelta(days=1)
                
            
            # as horas totais do período são as horas do total de dias do mes menos os finais de semana, ferias e folgas
            total_horas_periodo = (soma_dias_de_trabalho * 8 * 60 * 60)
            total_horas_periodo_str = '%2dh%2dmin' % (total_horas_periodo/3600, total_horas_periodo/60%60)
            
            total_horas_restante = total_horas_periodo - total;
            total_horas_restante_str = '%2dh%2dmin' % (total_horas_restante/3600, total_horas_restante/60%60)
            
            m.update({'total_horas_periodo':total_horas_periodo_str})
            m.update({'total_horas_restante':total_horas_restante_str})
        
        return TemplateResponse(request, 'membro/detalhe.html', {'meses':meses, 'membro':membro})
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

