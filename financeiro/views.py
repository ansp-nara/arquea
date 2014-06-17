# -* coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib import admin
from django.http import Http404, HttpResponse
from django.db.models import Q, Max
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Sum
from django.template import Context, loader, RequestContext
import json as simplejson
from decimal import Decimal
import datetime
import logging

from outorga.models import Modalidade, Outorga, Item, Termo, OrigemFapesp, Natureza_gasto, Acordo
from protocolo.models import Protocolo
from identificacao.models import Entidade, Identificacao
from rede.models import Recurso, PlanejaAquisicaoRecurso
from utils.functions import pega_lista, formata_moeda, render_to_pdf, render_to_pdf_weasy
from operator import itemgetter
from models import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

def termo_escolhido(request):
    if request.method == 'POST':
        termo_id = request.POST.get('termo_id')
        t = None
        try:
            t = Termo.objects.get(id=termo_id)
        except Termo.DoesNotExist:
            pass

        retorno = {}
        if t:
            protocolos = Protocolo.objects.filter(termo=t).order_by('tipo_documento', 'num_documento', 'data_vencimento')
            origens = OrigemFapesp.objects.filter(item_outorga__natureza_gasto__termo=t).order_by('acordo', 'item_outorga')
            prot = []
            for p in protocolos:
                prot.append({'pk':p.id, 'valor':p.__unicode__()})
            orig = []
            for o in origens:
                orig.append({'pk':o.id, 'valor':'%s - %s' % (o.acordo, o.item_outorga)})

            retorno = {'protocolos':prot, 'origens':orig}
        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")


def numero_escolhido(request):
    if request.method == 'POST':
        termo_id = request.POST.get('termo_id')
        numero = request.POST.get('numero')
        t = None
        if termo_id:
            try:
                t = Termo.objects.get(id=termo_id)
            except Termo.DoesNotExist:
                pass

        retorno = {}
        if t:
            protocolos = Protocolo.objects.filter(termo=t, num_documento__icontains=numero).order_by('tipo_documento', 'num_documento', 'data_vencimento')
        else:
            protocolos = Protocolo.objects.filter(num_documento__icontains=numero).order_by('tipo_documento', 'num_documento', 'data_vencimento')
        prot = []
        for p in protocolos:
            prot.append({'pk':p.id, 'valor':p.__unicode__()})
        retorno = {'protocolos':prot}
        json = simplejson.dumps(retorno)
    return HttpResponse(json,mimetype="application/json")

def codigo_escolhido(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')

        retorno = {}

        contas = ExtratoCC.objects.filter(cod_oper__icontains=codigo)
        ccs = []

        for c in contas:
            ccs.append({'pk':c.id, 'valor':c.__unicode__()})

        retorno = {'ccs': ccs}
        json = simplejson.dumps(retorno)
    
    return HttpResponse(json, mimetype="application/json")

def estrutura_pagamentos(pagamentos):

    total = pagamentos.aggregate(Sum('valor_fapesp'))
    por_modalidade = pagamentos.values('origem_fapesp__item_outorga__natureza_gasto').order_by('origem_fapesp__item_outorga__natureza_gasto').annotate(Sum('valor_fapesp'))
    pm = []
    for p in por_modalidade:
        pg = {}
        try:
            ng = Natureza_gasto.objects.get(id=p['origem_fapesp__item_outorga__natureza_gasto'])
            pg['modalidade'] = ng.modalidade.nome
            pg['total'] = formata_moeda(p['valor_fapesp__sum'], ',')
            pm.append(pg)
        except Natureza_gasto.DoesNotExist:
            pass

    pg = []
    for p in pagamentos.filter(conta_corrente__isnull=False).order_by('origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla').select_related('conta_corrente', 'protocolo', 'protocolo__tipo_documento', 'origem_fapesp__item_outorga__natureza_gasto__modalidade'):
        pp = {}
        pp['data'] = p.conta_corrente.data_oper.strftime('%d/%m/%Y')
        pp['termo'] = p.protocolo.termo.__unicode__()
        pp['oper'] = p.conta_corrente.cod_oper
        if p.protocolo.tipo_documento.nome.lower().find('anexo') == 0:
            pp['documento'] = '%s %s' % (p.protocolo.tipo_documento.nome, p.protocolo.num_documento)
        else:
            pp['documento'] = p.protocolo.num_documento
        pp['valor'] = formata_moeda(p.valor_fapesp, ',')
        try:
            pp['modalidade'] = p.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
        except: pp['modalidade'] = ''
        pag = 0
        ane = 0
        out = 0
        for a in p.auditoria_set.all().select_related('tipo'):
            if u'Comprovante de pag' in a.tipo.nome:
                pag = a
            elif u'Anexo' in a.tipo.nome:
                ane = a
            else: out = a

        if pag:
            pp['parcial'] = pag.parcial
            pp['pagina'] = pag.pagina
        elif ane:
            pp['parcial'] = ane.parcial
            pp['pagina'] = ane.pagina
        elif out:
            pp['parcial'] = out.parcial
            pp['pagina'] = out.pagina

        pg.append(pp)

    return {'pg':sorted(pg, key=itemgetter('modalidade', 'pagina')), 'pm':pm, 'total':total}
  
def parcial_pagina(request):
    if request.method == 'POST':
        orig = request.POST.get('orig_id')
        origem = get_object_or_404(OrigemFapesp, pk=orig)
        a = Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=origem.item_outorga.natureza_gasto).aggregate(Max('parcial'))
        parcial = a['parcial__max']
        a = Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=origem.item_outorga.natureza_gasto, parcial=parcial).aggregate(Max('pagina'))
        pagina = a['pagina__max']
        retorno = {'parcial':parcial, 'pagina':pagina+1}
        json = simplejson.dumps(retorno)

        return HttpResponse(json, mimetype="application/json")

@login_required
def nova_pagina(request):
    if request.method == 'POST':
        origem_id = request.POST.get('orig_id')
        parcial = request.POST.get('parcial')

        origem = get_object_or_404(OrigemFapesp, pk=origem_id)
        pagina = Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=origem.item_outorga.natureza_gasto, parcial=parcial).aggregate(Max('pagina'))
        pagina = 0 if pagina['pagina__max'] is None else pagina['pagina__max']

        retorno = pagina+1
        return HttpResponse(simplejson.dumps(retorno), mimetype="application/json")
  
@login_required
def pagamentos_mensais(request, pdf=False):

    if request.method == 'GET':
        if request.GET.get('ano'):
            ano = int(request.GET.get('ano'))
            mes = int(request.GET.get('mes'))
            pagamentos = Pagamento.objects.filter(conta_corrente__data_oper__month=mes,conta_corrente__data_oper__year=ano)
            dados = estrutura_pagamentos(pagamentos)

            if pdf:
                return render_to_pdf('financeiro/pagamentos.pdf', {'pagamentos':dados['pg'], 'ano':ano, 'mes':mes, 'total':formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm':dados['pm']}, filename='pagamentos.pdf')
            else:
                return render_to_response('financeiro/pagamentos.html', {'pagamentos':dados['pg'], 'ano':ano, 'mes':mes, 'total':formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm':dados['pm']}, context_instance=RequestContext(request))
        else:
            meses = range(1,13)
            anos = range(1990,datetime.datetime.now().year+1)
            anos.sort(reverse=True)
            return render_to_response('financeiro/pagamentos_mes.html', {'meses':meses, 'anos':anos}, context_instance=RequestContext(request))

@login_required
def pagamentos_parciais(request, pdf=False):
    if request.method == 'GET':
        if request.GET.get('parcial'):
            parcial = int(request.GET.get('parcial'))
            termo_id = int(request.GET.get('termo'))
            termo = Termo.objects.get(pk=termo_id)
            ids = [p.id for p in Pagamento.objects.filter(protocolo__termo=termo,auditoria__parcial=parcial).distinct()]
            pagamentos = Pagamento.objects.filter(id__in=ids)
            #for p in pagamentos:
            #	if p.auditoria_set.filter(parcial=parcial).count() == 0:
            #	    pagamentos = pagamentos.exclude(id=p.id)
            dados = estrutura_pagamentos(pagamentos)

            if pdf:
                return render_to_pdf('financeiro/pagamentos_parciais.pdf', {'pagamentos':dados['pg'], 'parcial':parcial, 'termo':termo, 'total':formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm':dados['pm']}, filename='pagamentos.pdf')
            else:
                return render_to_response('financeiro/pagamentos_parciais.html', {'pagamentos':dados['pg'], 'parcial':parcial, 'termo':termo, 'total':formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm':dados['pm']}, context_instance=RequestContext(request))
        else:
            parciais = range(1,21)
            termos = Termo.objects.all()
            return render_to_response('financeiro/pagamentos_parcial.html', {'parciais':parciais, 'termos':termos}, context_instance=RequestContext(request))
  
@login_required
def relatorio_gerencial(request, pdf=False):
    if request.method == 'GET':
        if request.GET.get('termo'):
            try:
                import locale
                locale.setlocale(locale.LC_ALL, 'pt_BR')
            except Exception:
                print ''
                
            id = int(request.GET.get('termo'))
            t = get_object_or_404(Termo,id=id)
            
            retorno = []
            meses = []
            totalizador = []
            
            ano = t.inicio.year
            afinal = (t.inicio+t.duracao()).year
            mes = t.inicio.month
            mfinal = (t.inicio+t.duracao()).month
            
            ultimo = Pagamento.objects.filter(protocolo__termo=t).aggregate(ultimo=Max('conta_corrente__data_oper'))
            ultimo = ultimo['ultimo']
            
            while ano < afinal or (ano <= afinal and mes <= mfinal):
                dt = datetime.date(ano,mes,1)
                meses.append(dt.strftime('%B de %Y').decode('latin1'))
                if ano == afinal and mes == mfinal:
                    dt2 = datetime.date(ano+5,mes,1)
                    total_real = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True, conta_corrente__data_oper__range=(dt,dt2)).aggregate(Sum('valor_fapesp'))
                    total_dolar = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False, protocolo__data_vencimento__range=(dt,dt2)).aggregate(Sum('valor_fapesp'))
                else:
                    total_real = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True, conta_corrente__data_oper__year=ano,conta_corrente__data_oper__month=mes).aggregate(Sum('valor_fapesp'))
                    total_dolar = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False, protocolo__data_vencimento__year=ano,protocolo__data_vencimento__month=mes).aggregate(Sum('valor_fapesp'))
                
                totalizador.append({'ord':dt.strftime('%Y%m'), 'total_real':total_real['valor_fapesp__sum'] or Decimal('0.0'), 'total_dolar':total_dolar['valor_fapesp__sum'] or Decimal('0.0')})
                
                mes += 1
                if mes > 12:
                    mes = 1
                    ano += 1
    
            cr = Natureza_gasto.objects.filter(termo=t, modalidade__moeda_nacional=True).exclude(modalidade__sigla='REI').aggregate(Sum('valor_concedido'))
            cr = cr['valor_concedido__sum'] or Decimal('0.0')
            
            cd = Natureza_gasto.objects.filter(termo=t, modalidade__moeda_nacional=False).exclude(modalidade__sigla='REI').aggregate(Sum('valor_concedido'))
            cd = cd ['valor_concedido__sum'] or Decimal('0.0')
            
            gr = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True).aggregate(Sum('valor_fapesp'))
            gr = gr['valor_fapesp__sum']  or Decimal('0.0')

            gd = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False).aggregate(Sum('valor_fapesp'))
            gd = gd['valor_fapesp__sum']  or Decimal('0.0')
            
            gerais = {'concedido_real': cr, 'concedido_dolar': cd, 'gasto_real': gr, 'gasto_dolar': gd, 'saldo_real': cr-gr, 'saldo_dolar': cd-gd}
            treal = {}
            tdolar = {}
            
            for ng in Natureza_gasto.objects.filter(termo=t).exclude(modalidade__sigla='REI').select_related('modalidade__moeda_nacional'):

                item = {'modalidade':ng.modalidade, 'concedido':ng.valor_concedido, 'realizado':ng.total_realizado, 'saldo':ng.valor_saldo(), 'meses':[], 'itens':{}, 'obs':ng.obs}
                for it in ng.item_set.all():
                    item['itens'].update({it:[]})

                ano = t.inicio.year
                afinal = (t.inicio+t.duracao()).year
                mes = t.inicio.month
                mfinal = (t.inicio+t.duracao()).month
                
                while ano < afinal or (ano <= afinal and mes <= mfinal):
                    total = Decimal('0.0')

                    if ng.modalidade.moeda_nacional:
                        sumFapesp = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto=ng, conta_corrente__data_oper__year=ano, conta_corrente__data_oper__month=mes).aggregate(Sum('valor_fapesp'))
                    else:
                        sumFapesp = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto=ng, protocolo__data_vencimento__year=ano, protocolo__data_vencimento__month=mes).aggregate(Sum('valor_fapesp'))

                    total += sumFapesp['valor_fapesp__sum'] or Decimal('0.0')
           
                    try:
                        dt = datetime.date(ano,mes+1,1)
                    except:
                        dt = datetime.date(ano+1, 1,1)
                    dt2 = datetime.date(ano+5,1,1)
                    if ano == afinal and mes == mfinal:
                        if ng.modalidade.moeda_nacional:
                            sumFapesp = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto=ng, conta_corrente__data_oper__range=(dt,dt2)).aggregate(Sum('valor_fapesp'))
                        else:
                            sumFapesp = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto=ng, protocolo__data_vencimento__range=(dt,dt2)).aggregate(Sum('valor_fapesp'))
                        total += sumFapesp['valor_fapesp__sum'] or Decimal('0.0')
                    dt = datetime.date(ano,mes,1)
                    item['meses'].append({'ord':dt.strftime('%Y%m'), 'data':dt.strftime('%B de %Y'),'valor':total})
                    for it in item['itens'].keys():
                        after = False
                        if ano == afinal and mes == mfinal: after = True

                        total = it.calcula_realizado_mes(dt, after)
                        item['itens'][it].append({'ord':dt.strftime('%Y%m'), 'valor': total})
                    mes += 1
                    if mes > 12:
                        mes = 1
                        ano += 1

                retorno.append(item)
    
            if pdf:
	            return render_to_pdf('financeiro/gerencial.pdf', {'atualizado':ultimo, 'termo':t, 'meses':meses, 'modalidades':retorno, 'totais':totalizador, 'gerais':gerais}, context_instance=RequestContext(request))
            else:
                return render_to_response('financeiro/gerencial.html', {'atualizado':ultimo, 'termo':t, 'meses':meses, 'modalidades':retorno, 'totais':totalizador, 'gerais':gerais}, context_instance=RequestContext(request))
        else:
            return render_to_response('financeiro/relatorios_termo.html', {'termos':Termo.objects.all()}, context_instance=RequestContext(request))

@login_required
def relatorio_acordos(request, pdf=False):
    if request.method == 'GET':
        if request.GET.get('termo'):
            id = int(request.GET.get('termo'))
            t = get_object_or_404(Termo,id=id)
            retorno = []
            
            for a in  Acordo.objects.all():
                ac = {'desc':a.__unicode__()}
                totalGeralReal = Decimal('0.0')
                totalGeralDolar = Decimal('0.0')
                itens = []

                for o in  a.origemfapesp_set.filter(item_outorga__natureza_gasto__termo=t).select_related('item_outorga', 'item_outorga__entidade'):
                    it = {'desc':'%s - %s' % (o.item_outorga.entidade, o.item_outorga.descricao), 'id':o.id}
                    totalReal = Decimal('0.0')
                    totalDolar = Decimal('0.0')
                    pg = []
                    for p in o.pagamento_set.order_by('conta_corrente__data_oper', 'id') \
                                            .select_related('conta_corrente', 'protocolo', 'protocolo__descricao2', 'protocolo__tipo_documento',\
                                                            'protocolo__descricao2__entidade','origem_fapesp__item_outorga__natureza_gasto__modalidade'):
                        
                        pags = {'p':p, 'docs':p.auditoria_set.select_related('tipo')}
                        pg.append(pags)

                        if p.origem_fapesp and p.origem_fapesp.item_outorga.natureza_gasto.modalidade.moeda_nacional == False:
                            totalDolar += p.valor_fapesp
                        else:
                            totalReal += p.valor_fapesp

                    it.update({'totalReal':totalReal, 'totalDolar':totalDolar, 'pg':pg})

                    totalGeralReal += totalReal
                    totalGeralDolar += totalDolar
                    itens.append(it)

                ac.update({'totalGeralReal':totalGeralReal, 'totalGeralDolar':totalGeralDolar, 'itens':itens})		
                retorno.append(ac)

            if pdf:
                return render_to_pdf_weasy(template_src='financeiro/acordos_weasy.pdf', context_dict={'termo':t, 'acordos':retorno}, filename='relatorio_de_acordos_da_outorga_%s.pdf'%t,)
            else:
                return render_to_response('financeiro/acordos.html', {'termo':t, 'acordos':retorno}, context_instance=RequestContext(request))
        else:
            return render_to_response('financeiro/relatorios_termo.html', {'termos':Termo.objects.all()}, context_instance=RequestContext(request))

@login_required
def extrato(request, pdf=False):

    if request.method == 'GET':
        if request.GET.get('ano'):
            ano = int(request.GET.get('ano'))
            retorno = []
            mes = 0
            for e in ExtratoCC.objects.filter(data_oper__year=ano).select_related('extrato_financeiro', 'extrato_financeiro__termo').order_by('data_oper', 'id'):
                if mes == 0:
                    mes = e.data_oper.month
                    retorno.append({'saldo_mes_anterior':e.saldo_anterior, 'data':e.data_oper})
                if e.data_oper.month==mes:
                    retorno.append(e)
                else:
                    if retorno:
                        e1 = retorno[-1]
                        retorno.append({'saldo':e1.saldo, 'data':e1.data_oper})
                    retorno.append(e)
                    mes = e.data_oper.month
            if retorno:
                e1 = retorno[-1]
                retorno.append({'saldo':e1.saldo, 'data':e1.data_oper})

            if pdf:
                return render_to_pdf_weasy('financeiro/contacorrente.pdf', {'ano':ano, 'extrato':retorno}, filename='extrato_cc_%s.pdf' % ano)
            else:
                return render_to_response('financeiro/contacorrente.html', {'ano':ano, 'extrato':retorno}, context_instance=RequestContext(request))
        else:
            anos = range(1990,datetime.datetime.now().year+1)
            anos.sort(reverse=True)
            return render_to_response('financeiro/sel_contacorrente.html', {'anos':anos}, context_instance=RequestContext(request))	    


@login_required
def extrato_mes(request, pdf=False):

    if request.method == 'GET':
        if request.GET.get('ano'):
            ano = int(request.GET.get('ano'))
            mes = int(request.GET.get('mes'))
            retorno = []
            sa = True
            for e in ExtratoCC.objects.filter(data_oper__year=ano, data_oper__month=mes).order_by('data_oper', 'id'):
                if sa:
                    sa = False
                    retorno.append(e.saldo_anterior)
                retorno.append(e)
            if retorno:
                e1 = retorno[-1]
                retorno.append(e1.saldo)

            if pdf:
                return render_to_pdf('financeiro/contacorrente_mes.pdf', {'ano':ano, 'mes':mes, 'extrato':retorno}, filename='extrato_cc_%s/%s.pdf' % (mes,ano))
            else:
                return render_to_response('financeiro/contacorrente_mes.html', {'ano':ano, 'mes':mes, 'extrato':retorno}, context_instance=RequestContext(request))
        else:
            meses = range(1,13)
            anos = range(1990,datetime.datetime.now().year+1)
            anos.sort(reverse=True)
            return render_to_response('financeiro/sel_contacorrente_mes.html', {'anos':anos, 'meses':meses}, context_instance=RequestContext(request))	    

@login_required
def extrato_financeiro(request, ano=datetime.datetime.now().year, pdf=False):

    if request.method == 'GET':
        if request.GET.get('termo'):
            termo_id = int(request.GET.get('termo'))
            termo = get_object_or_404(Termo, id=termo_id)
            mes = int(request.GET.get('mes'))
            if mes:
                efs = ExtratoFinanceiro.objects.filter(termo=termo, data_libera__month=mes)
            else:
                efs = ExtratoFinanceiro.objects.filter(termo=termo)
            extrato = []
            for ef in efs.order_by('data_libera'):
                ex = {'data':ef.data_libera, 'cod':ef.cod, 'historico':ef.historico, 'valor':ef.valor, 'comprovante':ef.comprovante, 'cheques':[]}
                total = Decimal('0.0')
                for c in ef.extratocc_set.all():
                    valor = c.pagamento_set.aggregate(Sum('valor_fapesp'))
                    total += valor['valor_fapesp__sum'] or Decimal('0.0')
                    parciais = []
                    for p in c.pagamento_set.all():
                        for a in p.auditoria_set.all():
                            if not a.parcial in parciais:
                                parciais.append(a.parcial)

                    ch = {'id':c.id, 'valor':c.valor, 'cod': c.cod_oper, 'parciais':', '.join([str(p) for p in parciais])}
                    ex['cheques'].append(ch)
                ex['diferenca'] = ef.valor+total
                extrato.append(ex)

            if pdf:
                return render_to_pdf('financeiro/financeiro.pdf', {'ano':ano, 'extrato':extrato}, filename='financeiro_%s/%s.pdf' % (mes,ano))
            else:
                return render_to_response('financeiro/financeiro.html', {'termo':termo, 'mes':mes, 'ano':ano, 'extrato':extrato}, context_instance=RequestContext(request))
        else:
            meses = range(0,13)
            return render_to_response('financeiro/relatorios_termo.html', {'termos':Termo.objects.all(), 'meses':meses}, context_instance=RequestContext(request))

@login_required
def extrato_tarifas(request, pdf=False):
    if request.method == 'GET':
        if request.GET.get('ano'):
            ano = int(request.GET.get('ano'))
            mes = int(request.GET.get('mes'))
            if mes == 0:
                tars = ExtratoCC.objects.filter(Q(data_oper__year=ano), Q(historico__icontains='tar')|Q(historico__icontains='crédito aut')|Q(historico__icontains='juro')).order_by('data_oper')
            else:
                tars = ExtratoCC.objects.filter(Q(data_oper__month=mes), Q(data_oper__year=ano), Q(historico__icontains='tar')|Q(historico__icontains='créditto aut')|Q(historico__icontains='juro')).order_by('data_oper')
            total = tars.aggregate(Sum('valor'))

            context = {'total':total['valor__sum'], 'ano':ano, 'tarifas':tars}
            if mes > 0: context.update({'mes':mes})
            if pdf:
                return render_to_pdf('financeiro/tarifas.pdf', context, filename='tarifas_%s/%s.pdf' % (mes,ano))
            else:
                return render_to_response('financeiro/tarifas.html', context, context_instance=RequestContext(request))
        else:
            meses = range(0,13)
            anos = range(1990,datetime.datetime.now().year+1)
            anos.sort(reverse=True)
            return render_to_response('financeiro/pagamentos_mes.html', {'anos':anos, 'meses':meses}, context_instance=RequestContext(request))

	    

@login_required
def cheque(request, cc=1):
    extrato = get_object_or_404(ExtratoCC, id=cc)
    if not extrato.extrato_financeiro: raise Http404
    termo = extrato.extrato_financeiro.termo

    #return render_to_response('financeiro/cheque.pdf', {'cc':extrato, 'termo':termo})
    return render_to_pdf('financeiro/cheque.pdf', {'cc':extrato, 'termo':termo}, filename='capa_%s.pdf' % extrato.cod_oper)


@login_required
def financeiro_parciais(request, pdf=False):
    if request.method == 'GET':
        if request.GET.get('termo'):
            termo_id = int(request.GET.get('termo'))
            rt = bool(request.GET.get('rt'))
	    if rt:
		codigo = 'RP'
	    else:
		codigo = 'MP'
            termo = get_object_or_404(Termo, id=termo_id)
            retorno = []
            parciais = ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo).distinct('parcial').values_list('parcial', flat=True).order_by('parcial')
            
            for parcial in parciais:
                extrato = []
                
                liberado = Decimal('0.0')
                devolvido = Decimal('0.0')
                concedido = Decimal('0.0')
                suplementado = Decimal('0.0')
                anulado = Decimal('0.0')
                estornado = Decimal('0.0')
                cancelado = Decimal('0.0')
                
                liberacoes = ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo, parcial=parcial).values('cod').annotate(Sum('valor')).order_by()
                
                for t in liberacoes:
                    if t['cod'] == 'PGMP' or t['cod'] == 'PGRP': liberado = t['valor__sum'] or Decimal('0.0')
                    elif t['cod'] == 'DVMP' or t['cod'] == 'DVRP': devolvido= t['valor__sum'] or Decimal('0.0')
                    elif t['cod'] == 'COMP' or t['cod'] == 'CORP': concedido= t['valor__sum'] or Decimal('0.0')
                    elif t['cod'] == 'SUMP' or t['cod'] == 'SURP': suplementado= t['valor__sum'] or Decimal('0.0')
                    elif t['cod'] == 'ANMP' or t['cod'] == 'ANRP': anulado= t['valor__sum'] or Decimal('0.0')
                    elif t['cod'] == 'ESMP' or t['cod'] == 'ESRP': estornado= t['valor__sum'] or Decimal('0.0')
                    elif t['cod'] == 'CAMP' or t['cod'] == 'CARP': cancelado= t['valor__sum'] or Decimal('0.0')
                    
                pagamentos = liberado+devolvido+estornado
                concessoes = concedido+suplementado+anulado+cancelado
                diferenca_total = Decimal('0.0')
                anterior = datetime.date(1971,1,1)
                tdia = Decimal('0.0')
                exi = {}
                for ef in ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo, parcial=parcial).prefetch_related('extratocc_set').order_by('data_libera', '-historico'):
                    if ef.data_libera > anterior:
                        ex = {'data':ef.data_libera}
                        anterior = ef.data_libera
                        if exi:
                            exi.update({'valor_data':tdia})
                        exi = ex
                        tdia = ef.valor
                    else:
                        ex = {'data':''}
                        if ef.cod == 'PGMP':
                            tdia += ef.valor
                        else:
                            ex = {'data':ef.data_libera}
                    ex.update({'cod':ef.cod, 'historico':ef.historico, 'valor':ef.valor, 'comprovante':ef.comprovante, 'cheques':[]})
                    total = Decimal('0.0')
                    tcheques = Decimal('0.0')
                    for c in ef.extratocc_set.all():
                        v_fapesp = Decimal('0.0')
                        #total += c.valor
                        tcheques += c.valor
                        mods = {}
                        for p in c.pagamento_set.all().prefetch_related('auditoria_set').select_related('origem_fapesp', 'origem_fapesp__item_outorga__natureza_gasto__modalidade'):
                            if not p.origem_fapesp: continue
                            v_fapesp += p.valor_fapesp
                            modalidade = p.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
                            if modalidade not in mods.keys():
                                mods[modalidade] = {}
                            for a in p.auditoria_set.all():
                                if not a.parcial in mods[modalidade].keys():
                                    mods[modalidade][a.parcial] = []
                                if not a.pagina in mods[modalidade][a.parcial]:
                                    mods[modalidade][a.parcial].append(a.pagina)
                        total -= v_fapesp
                        parc = ''
                        for modalidade in mods.keys():
                            parc += '%s [parcial ' % modalidade
                            pags = []
                            if len(mods[modalidade].keys()) > 0:
                                for p in mods[modalidade].keys():
                                    pags= mods[modalidade][p]
                                    pags.sort()
                            parc += '%s (%s)' % (p, ','.join([str(k) for k in pags]))
                            parc += ']       '
                            
                        ch = {'id':c.id, 'valor':c.valor, 'cod': c.cod_oper, 'parciais':parc, 'obs':c.obs}

                        if v_fapesp != c.valor:
                            ch.update({'v_fapesp':v_fapesp})
                        ex['cheques'].append(ch)
                    if ef.cod == 'PGMP' or ef.cod == 'DVMP' or ef.cod == 'ESMP':
                        ex['diferenca'] = ef.valor-total
                        diferenca_total += ef.valor-total
                    if total > ef.valor: 
                        ex['cor'] = 'red'
                    else: 
                        ex['cor'] = 'blue'
                    if tcheques != ef.valor and ef.cod == 'PGMP':
                        ex['patrocinio'] = tcheques - ef.valor
                    extrato.append(ex)
                if exi: 
                    exi.update({'valor_data':tdia})
                retorno.append({'parcial':str(parcial), 'extrato':extrato, 'liberado':-liberado, 
                                'devolvido':devolvido, 'pagamentos':-pagamentos, 
                                'diferenca_total':diferenca_total,  'concedido':concedido, 
                                'suplementado':suplementado, 'anulado':anulado, 
                                'cancelado':cancelado, 'concessoes':concessoes, 
                                'estornado':estornado})
                
                total_liberado = 0
                total_devolvido = 0
                total_estornado = 0
                total_pagamentos = 0
                total_diferenca_total = 0
                
                total_concedido = 0
                total_suplementado = 0
                total_anulado = 0
                total_cancelado = 0
                total_concessoes = 0
                
                for r in retorno:
                    total_liberado += r['liberado']
                    total_devolvido += r['devolvido']
                    total_estornado += r['estornado']
                    total_pagamentos += r['pagamentos']
                    total_diferenca_total += r['diferenca_total']
                    
                    total_concedido += r['concedido']
                    total_suplementado += r['suplementado']
                    total_anulado += r['anulado']
                    total_cancelado += r['cancelado']
                    total_concessoes += r['concessoes']

                totais={'total_liberado':total_liberado, 'total_devolvido':total_devolvido,
                          'total_estornado':total_estornado, 'total_pagamentos':total_pagamentos,
                          'total_diferenca_total':total_diferenca_total,
                        'total_concedido':total_concedido, 'total_suplementado':total_suplementado,
                          'total_anulado':total_anulado, 'total_cancelado':total_cancelado,
                          'total_concessoes':total_concessoes, }
            
            if pdf:
                return render_to_pdf_weasy('financeiro/financeiro_parcial.pdf', {'size':pdf, 'termo':termo, 'parciais':retorno, 'totais':totais}, filename='financeiro_parciais_%s.pdf' % termo.__unicode__())
            else:
                return render_to_response('financeiro/financeiro_parcial.html', {'termo':termo, 'parciais':retorno, 'totais':totais}, context_instance=RequestContext(request))
        else:
            return render_to_response('financeiro/relatorios_termo.html', {'termos':Termo.objects.all()}, context_instance=RequestContext(request))

@login_required
def parciais(request, caixa=False, pdf=False):
    if request.method == 'GET':
        if request.GET.get('termo'):
            termo_id = int(request.GET.get('termo'))
            termo = get_object_or_404(Termo, id=termo_id)
            retorno = []

            for parcial in Auditoria.objects.filter(pagamento__protocolo__termo=termo).values_list('parcial', flat=True).distinct():
                parcs = {'parcial':parcial}
                ads = Auditoria.objects.filter(parcial=parcial, pagamento__protocolo__termo=termo) 
    
#                 pgs = []
#                 for a in ads:
#                     if caixa:
#                         if a.pagamento.conta_corrente and a.pagamento.conta_corrente.despesa_caixa and a.pagamento not in pgs:
#                             pgs.append(a.pagamento)
#                         else:
#                             if a.pagamento not in pgs:
#                                 pgs.append(a.pagamento)

                ch = ExtratoCC.objects.filter(extrato_financeiro__parcial=parcial, extrato_financeiro__termo=termo)
                if caixa: ch = ch.filter(despesa_caixa=True)

        #for p in pgs:
        #    if p.conta_corrente and p.conta_corrente not in ch:
    #        ch.append(p.conta_corrente)
            
            
                ret = []
                total_diff = Decimal('0.0')
                for ecc in ch:
                    pagos = ecc.pagamento_set.aggregate(Sum('valor_fapesp'))
                    pago = pagos['valor_fapesp__sum'] or Decimal('0.0')
                    pagos = ecc.pagamento_set.aggregate(Sum('valor_patrocinio'))
                    #pago = pago + (pagos['valor_patrocinio__sum'] or Decimal('0.0'))
                    diff = ecc.valor+pago
                    total_diff += diff
                    este = {'cheque':ecc, 'diff':-diff}
                    pgtos = []
                    for p in ecc.pagamento_set.all().select_related('protocolo', 'origem_fapesp__item_outorga__natureza_gasto', 'origem_fapesp__item_outorga__natureza_gasto__modalidade', 'origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla'):
                        ok = True
                        for a in p.auditoria_set.distinct('parcial'):
                            if a.parcial != parcial:
                                ok = False
                                break
                        pgtos.append({'pg':p, 'naparcial':ok})
                    este.update({'pgtos':pgtos})
                    
                    ret.append(este)
    
                parcs.update({'dados':ret, 'diff':-total_diff})
                retorno.append(parcs)

            if pdf:
                return render_to_pdf('financeiro/parciais.pdf', {'parciais':retorno, 'termo':termo}, filename='parciais.pdf')
            else:
                return render_to_response('financeiro/parciais.html', {'caixa':caixa, 'parciais':retorno, 'termo':termo}, context_instance=RequestContext(request))
        else:
            return render_to_response('financeiro/relatorios_termo.html', {'termos':Termo.objects.all()}, context_instance=RequestContext(request))

def escolhe_extrato(request):
    if request.method == 'POST':
        termo_id = request.POST.get('termo')
        termo = get_object_or_404(Termo, id=termo_id)

    ef = ExtratoFinanceiro.objects.filter(termo=termo)
    extratos = []
    for e in ef:
        extratos.append({'pk':e.id, 'valor':e.__unicode__()})

    json = simplejson.dumps(extratos)
    return HttpResponse(json, mimetype="application/json")


@login_required
def presta_contas(request, pdf=False):
    if request.method == 'GET':
        if request.GET.get('termo'):
            termo_id = request.GET.get('termo')
            termo = get_object_or_404(Termo, id=termo_id)
            m = []
            for ng in Natureza_gasto.objects.filter(termo=termo).select_related('modalidade'):
                mod = {'modalidade':ng.modalidade.nome}
                parcs = []
                for p in Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=ng).values_list('parcial', flat=True).distinct():
                    pgtos = []
                    pag = None
                    for a in Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=ng, parcial=p).order_by('pagina').select_related('pagamento', 'pagamento__protocolo', 'pagamento__origem_fapesp__item_outorga', 'pagamento__conta_corrente', 'pagamento__extrato_financeiro', 'pagamento__conta_corrente__extrato_financeiro__comprovante'):
                        auditorias = []
                        if a.pagamento != pag:
                            pgtos.append({'pg':a.pagamento, 'pagina':a.pagina, 'auditorias':auditorias})
                            pag = a.pagamento
                        
                            for auditoria in a.pagamento.auditoria_set.all().select_related('tipo', 'estado', 'arquivo'):
                                auditorias.append({'auditoria':auditoria}) 
                        
                    parcs.append({'num':p, 'pgtos':pgtos})
                mod.update({'parcial':parcs})
                m.append(mod)
            if pdf:
               return render_to_pdf('financeiro/presta_contas.pdf', {'modalidades':m, 'termo':termo}, filename='presta_contas_%s.pdf' % termo.__unicode__(), context_instance=RequestContext(request))
            else:
               return render_to_response('financeiro/presta_contas.html', {'modalidades':m, 'termo':termo}, context_instance=RequestContext(request))
        else:
            return render_to_response('financeiro/relatorios_termo.html', {'termos':Termo.objects.all()}, context_instance=RequestContext(request))


@login_required
def tipos_documentos(context):
 
    protocolos = []
    for p in Protocolo.objects.filter(pagamento__isnull=False):
	ads = Auditoria.objects.filter(pagamento__protocolo=p)
        audits = []
        for a in ads:
            aa = {'tipo':a.tipo.nome}
            if a.arquivo: aa.update({'arquivo':a.arquivo.url})
            if a.pagamento.conta_corrente: aa.update({'pagamento':a.pagamento.conta_corrente.cod_oper})
            audits.append(aa)
        protocolos.append({'tipo':p.tipo_documento.nome, 'auditorias':audits})

    return render_to_response('financeiro/tipos.html', {'protocolos':protocolos})

def ajax_get_recursos_vigentes(request):
    """
    AJAX para buscar os dados dos recursos.
    Recebe parametro para filtra por estado (ex: Vigente) ou buscar todos os registros
    """
    estado = request.GET.get('estado') or request.POST.get('estado')
    print estado
    retorno = []
    if estado and estado != '':
        recursos = PlanejaAquisicaoRecurso.objects.filter(os__estado__nome=estado).select_related('os', 'os__tipo', 'projeto', 'tipo', )
    else:
        recursos = PlanejaAquisicaoRecurso.objects.all().select_related('os', 'os__tipo', 'projeto', 'tipo', )
        
    retorno = [{'pk':r.pk, 'valor':r.__unicode__()}
               for r in recursos]
    
    json = simplejson.dumps(retorno)
    return HttpResponse(json, mimetype="application/json")
