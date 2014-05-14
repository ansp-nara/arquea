from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
import json as simplejson

from utils.functions import render_to_pdf
from outorga.models import *
from financeiro.models import Pagamento
from identificacao.models import Entidade, Identificacao, ASN
from models import *
from modelsResource import *


# Create your views here.
def escolhe_pagamento(request):
    if request.method == 'POST':
        retorno = []
        termo = request.POST.get('termo')

        if termo:
            for p in Pagamento.objects.filter(protocolo__termo__id=termo):
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

@login_required
def planejamento(request, pdf=0):

    anoproj = request.GET.get('anoproj')
    if anoproj:
        ano, proj = anoproj.split('/')
    else:
        ano = None
        proj = None
    contrato = request.GET.get('contrato')
    os = request.GET.get('os')

    if not ano and not proj and not contrato and not os:
        return TemplateResponse(request, 'rede/escolhe_ano.html', {'anoproj': [(p[0], Projeto.objects.get(id=p[1])) for p in PlanejaAquisicaoRecurso.objects.values_list('ano', 'projeto').order_by('ano').distinct()], 'oss':OrdemDeServico.objects.all()})

    entidades = []

    for e in Entidade.objects.filter(contrato__ordemdeservico__planejaaquisicaorecurso__isnull=False).distinct():
        entidade = {'entidade':e}
        planejamentos = PlanejaAquisicaoRecurso.objects.filter(os__contrato__entidade=e)
        if ano: planejamentos = planejamentos.filter(ano=ano)
        if proj: planejamentos = planejamentos.filter(projeto__id=proj)
        if os: planejamentos = planejamentos.filter(os__id=os)
        projetos = []
        for p in Projeto.objects.filter(planejaaquisicaorecurso__in=planejamentos).distinct():
            projeto = {'projeto':p, 'plan':planejamentos.filter(projeto=p)}
            projetos.append(projeto)
        entidade.update({'projetos':projetos})
        entidades.append(entidade)

    if pdf:
	return render_to_pdf('rede/planejamento.pdf', {'entidades':entidades, 'ano':ano}, filename='planejamento%s.pdf' % ano)
    return TemplateResponse(request, 'rede/planejamento.html', {'entidades':entidades, 'ano':ano, 'projeto':proj, 'os':os})

@login_required
def planilha_informacoes_gerais(request):
    info = Enlace.objects.filter(participante__entidade__entidadehistorico__ativo=True)
    return TemplateResponse(request, 'rede/informacoes_gerais.html', {'info': info})

@login_required
def planilha_informacoes_tecnicas(request, id=None):
    if not id: raise Http404
    tecnicos = Identificacao.objects.filter(area__contains='Tec')
    adm = Identificacao.objects.filter(Q(area__contains='Adm')|Q(area__contains='Gest'))	
    asns = ASN.objects.all() #filter(pais='BR')
    blocos_ips = BlocoIP.objects.all()
    dados = []
    for e in Enlace.objects.filter(id=id): 
        entidade = e.participante.entidade
        contato_tec = tecnicos.filter(endereco__entidade=entidade)
        contato_adm = adm.filter(endereco__entidade=entidade)
        asn = asns.filter(entidade=entidade)
        blocos = blocos_ips.filter(designado=entidade)
        #operadoras = e.enlaceoperadora_set.all()
	operadoras = e.segmento_set.filter(data_desativacao__isnull=True)
        dados.append({"enlace":e, "contatos_tec":contato_tec, "contatos_adm":contato_adm, "asn":asn, "bloco_ip":blocos, "operadoras":operadoras})
    return TemplateResponse(request, 'rede/informacoes_tecnicas.html', {'dados': dados})

@login_required
def imprime_informacoes_gerais(request):
    contatos = request.GET.get('contatos')
    info = []
    tecnicos = Identificacao.objects.filter(area__contains='Tec')
    asns = ASN.objects.all() #filter(pais='BR')
    blocos_ips = BlocoIP.objects.all()
    for e in Enlace.objects.filter(participante__entidade__entidadehistorico__ativo=True):
	entidade = e.participante.entidade
        if contatos: contato_tec = tecnicos.filter(endereco__entidade=entidade)
        else: contato_tec = None
        asn = asns.filter(entidade=entidade)
        blocos = blocos_ips.filter(designado=entidade)
        operadoras = e.segmento_set.filter(data_desativacao__isnull=True)
        info.append({'info':e, "contatos_tec":contato_tec, "asn":asn, "bloco_ip":blocos, "operadoras":operadoras})

    return render_to_pdf('rede/informacoes_gerais.pdf', {'info':info}, filename='informacoes_gerais.pdf')


@login_required
def blocos_texto(request):
    return TemplateResponse(request, 'rede/blocos.txt', {'blocos':BlocoIP.objects.all()}, content_type='text/plain')


def planeja_contrato(request):

    if request.method == 'POST':
        ano = request.POST.get('ano')
        proj_id = request.POST.get('proj_id')

        os_ids = PlanejaAquisicaoRecurso.objects.filter(ano=ano, projeto__id=proj_id).order_by('os').values_list('os', flat=True)
        oss = [{'pk':o.id, 'valor':'%s - %s' % (o.contrato, o)} for o in OrdemDeServico.objects.filter(id__in=os_ids)]
        json = simplejson.dumps({'oss':oss})

        return HttpResponse(json,mimetype="application/json")

@login_required
def planejamento2(request, pdf=0):
    
    entidade_id = request.GET.get('entidade')
    termo_id = request.GET.get('termo')
    if entidade_id and termo_id:
	entidade = Entidade.objects.filter(id=entidade_id)
	termo = Termo.objects.filter(id=termo_id)
    else:
	entidade = None
	termo = None

    beneficiado_id = request.GET.get('beneficiado')
    if beneficiado_id: beneficiado = Entidade.objects.filter(id=beneficiado_id)
    else: beneficiado = None
    descricoes_ids = request.GET.getlist('tiposervico')
    if entidade and termo:
        igeral = Decimal('0.0')
        tgeral = Decimal('0.0')
        if beneficiado: beneficiado = beneficiado[0]
        entidade = entidade[0]
        termo = termo[0]
        pagamentos = []
        pgs = Pagamento.objects.filter(recurso__id__isnull=False, protocolo__termo=termo).distinct()
        if beneficiado: pgs = pgs.filter(recurso__planejamento__beneficiado__entidade=beneficiado)
        if descricoes_ids: pgs = pgs.filter(recurso__planejamento__tipo__id__in=descricoes_ids)
        for p in pgs:
            imposto = Decimal('0.0')
            total = Decimal('0.0')
            recursos = []
            rcs = p.recurso_set.filter(planejamento__os__contrato__entidade=entidade)
            if beneficiado: rcs = rcs.filter(planejamento__beneficiado__entidade=beneficiado)
            if descricoes_ids: rcs = rcs.filter(planejamento__tipo__id__in=descricoes_ids)
            for r in rcs:
                if beneficiado:
		    b = r.planejamento.beneficiado_set.get(entidade=beneficiado)
                imposto += Decimal(str(r.quantidade))*r.valor_imposto_mensal*Decimal(str(b.porcentagem()/100)) if beneficiado else Decimal(str(r.quantidade))*r.valor_imposto_mensal
                total += Decimal(str(r.quantidade))*r.valor_mensal_sem_imposto*Decimal(str(b.porcentagem()/100)) if beneficiado else Decimal(str(r.quantidade))*r.valor_mensal_sem_imposto
                unitario_sem = r.valor_mensal_sem_imposto*Decimal(str(b.porcentagem()/100)) if beneficiado else r.valor_mensal_sem_imposto
                unitario_com = r.valor_imposto_mensal*Decimal(str(b.porcentagem()/100)) if beneficiado else r.valor_imposto_mensal
                sub_sem = Decimal(str(r.quantidade)) * unitario_sem
		sub_com = Decimal(str(r.quantidade)) * unitario_com
                recursos.append({'os':r.planejamento.os, 'quantidade':r.quantidade, 'sem':unitario_sem, 'com':unitario_com, 'sub_sem':sub_sem, 'sub_com':sub_com, 'tipo':r.planejamento.tipo, 'referente':r.planejamento.referente, 'beneficiados':None if beneficiado else r.planejamento.beneficiado_set.all() })
            pagamentos.append({'nf':p.protocolo.num_documento, 'sem':total, 'com':imposto, 'recursos':recursos})
            igeral += imposto
            tgeral += total
        if pdf:
	    return render_to_pdf('rede/planejamento2.pdf', {'beneficiado':beneficiado, 'entidade':entidade, 'termo':termo, 'pagamentos':pagamentos, 'sem':tgeral, 'com':igeral})
        else:
            return TemplateResponse(request, 'rede/planejamento2.html', {'beneficiado':beneficiado, 'entidade':entidade, 'termo':termo, 'pagamentos':pagamentos, 'sem':tgeral, 'com':igeral, 'servicos':descricoes_ids})
    else:
        return TemplateResponse(request, 'rede/escolhe_entidade_termo.html', {'entidades':Entidade.objects.filter(contrato__ordemdeservico__planejaaquisicaorecurso__id__isnull=False).distinct(), 'termos':Termo.objects.all(), 'beneficiados':Entidade.objects.all(), 'descricoes':TipoServico.objects.order_by('nome')})



@login_required
def blocos_ip(request):
    if request.method != 'GET':
	raise Http404

    if len(request.GET) < 4:
        ent_usuario_ids = BlocoIP.objects.values_list('usuario', flat=True).distinct()
        ent_designado_ids = BlocoIP.objects.values_list('designado', flat=True).distinct()
        return TemplateResponse(request, 'rede/filtra_blocos.html', {'asns':ASN.objects.all(), 'usuarios':Entidade.objects.filter(id__in=ent_usuario_ids), 'designados':Entidade.objects.filter(id__in=ent_designado_ids)})

    else:
        blocos = BlocoIP.objects.all()

        anunciante = request.GET.get('anunciante')
        if anunciante != '0':
	    blocos = blocos.filter(asn__id=anunciante)

        proprietario = request.GET.get('proprietario')
        if proprietario != '0':
            blocos = blocos.filter(proprietario__id=proprietario)

        usuario = request.GET.get('usuario')
        if usuario != '0':
            blocos = blocos.filter(usuario__id=usuario)

        designado = request.GET.get('designado')
        if designado != '0':
            blocos = blocos.filter(designado__id=designado)

        if request.GET.get('porusuario'):
            return TemplateResponse(request, 'rede/blocosip.html.notree', {'blocos':blocos.order_by('usuario__sigla')})
        return TemplateResponse(request, 'rede/blocosip.html', {'blocos':blocos})
     
@login_required
def custo_terremark(request, pdf=0, xls=0):
    recursos = Recurso.objects.order_by('planejamento__os', 'planejamento__tipo')
    
    if request.GET.get('xls') and request.GET.get('xls')=='1':
        # Export para Excel/XLS
        recursos = Recurso.objects.order_by('planejamento__os', 'planejamento__tipo')
        dataset = CustoTerremarkRecursoResource().export(queryset=recursos)
        
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=custo_terremark.xls"

        return response
        
    elif pdf:
        # Export para PDF
        return render_to_pdf(template_src='rede/tabela_terremark.pdf', context_dict={'recursos':recursos, }, filename='custos_dos_recursos_contratados.pdf')
        
    return TemplateResponse(request, 'rede/tabela_terremark.html', {'recursos':recursos})
