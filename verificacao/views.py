# -* coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q, Max, Sum, Count 
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from django.template.response import TemplateResponse

from models import *
from verificacao.models import VerificacaoEquipamento
from patrimonio.models import Tipo
import datetime
import json as simplejson
import os


import logging
from patrimonio.models import Equipamento, Patrimonio
from django.db.models import Q, Max, Sum, Count

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def equipamento_consolidado(request):
    retorno = []
        
    verificacaoEquipamento = VerificacaoEquipamento()
    
    partNumberVSModeloDiferente = verificacaoEquipamento.partNumberVSModeloDiferente()
    count = sum([len(equipamentos) for equipamentos in partNumberVSModeloDiferente])
    retorno.append({'desc':u'Part Numbers iguais com Modelos diferentes', 'url':'equipamento_part_number_modelo_diferente', 'qtd':count})
    
    partNumberVazio = verificacaoEquipamento.partNumberVazio()
    count = sum([len(equipamentos) for equipamentos in partNumberVazio])
    retorno.append({'desc':u'Part Numbers vazios', 'url':'equipamento_part_number_vazio', 'qtd':count})
    
    partNumberVazioModeloVazio = verificacaoEquipamento.partNumberVazioModeloVazio()
    count = sum([len(equipamentos) for equipamentos in partNumberVazioModeloVazio])
    retorno.append({'desc':u'Part Numbers e Modelos vazios', 'url':'equipamento_part_number_modelo_vazio', 'qtd':count})
    
    marcaVazia = verificacaoEquipamento.marcaVazia()
    count = len(marcaVazia)
    retorno.append({'desc':u'Marca/Entidade vazia', 'url':'equipamento_marca_vazia', 'qtd':count})
    
    return render_to_response('verificacao/equipamento_consolidado.html', {'verificacoes':retorno}, context_instance=RequestContext(request))

@login_required
def equipamento_marca_vazia(request, json=False):

    retorno = []
    verficacao = VerificacaoEquipamento()
    retorno = verficacao.marcaVazia()
    
    return render_to_response('verificacao/equipamento_marca.html', 
                              {'desc':'Marca/Entidade vazia', 'equipamentos':retorno}, 
                              context_instance=RequestContext(request))


@login_required
def equipamento_part_number_modelo_diferente(request, json=False):

    retorno = []
    verficacao = VerificacaoEquipamento()
    retorno = verficacao.partNumberVSModeloDiferente()
    
    return render_to_response('verificacao/equipamento_part_number.html', 
                              {'desc':'Part Numbers iguais com Modelos diferentes', 'equipamentos':retorno}, 
                              context_instance=RequestContext(request))



@login_required
def equipamento_part_number_vazio(request, json=False):

    retorno = []
    verficacao = VerificacaoEquipamento()
    retorno = verficacao.partNumberVazio()
    
    return render_to_response('verificacao/equipamento_part_number.html', 
                              {'desc':'Part Numbers vazios', 'equipamentos':retorno}, 
                              context_instance=RequestContext(request))


@login_required
def equipamento_part_number_modelo_vazio(request, json=False):

    retorno = []
    verficacao = VerificacaoEquipamento()
    retorno = verficacao.partNumberVazioModeloVazio()
    
    return render_to_response('verificacao/equipamento_part_number.html', 
                              {'desc':'Part Numbers e Modelos vazios', 'equipamentos':retorno}, 
                              context_instance=RequestContext(request))
    

@login_required
def check_patrimonio_equipamento(request):

   
    patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).select_related('equipamento')
    
    patrimonios = patrimonios.filter(~Q(equipamento__part_number=F('part_number'))|
                                     ~Q(equipamento__modelo=F('modelo'))|
                                     ~Q(equipamento__entidade_fabricante__sigla=F('marca'))|
                                     #~Q(equipamento__descricao=F('descricao')) |
                                     Q(~Q(equipamento__ean=F('ean')), Q(equipamento__ean__isnull=False), Q(ean__isnull=False)) |
                                     Q(~Q(equipamento__ncm=F('ncm')), Q(equipamento__ncm__isnull=False), Q(ncm__isnull=False)) |
                                     Q(~Q(equipamento__tamanho=F('tamanho')), Q(equipamento__tamanho__isnull=False), Q(tamanho__isnull=False)) 
                                     )
    c = {}
    c.update({'patrimonios': patrimonios})
    
    return TemplateResponse(request, 'verificacao/check_patrimonio_equipamento.html', c)
    
    
@login_required
def patrimonio_consolidado(request):
    retorno = []
        
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}
        
    verificacaoPatrimonio = VerificacaoPatrimonio()
    
    equipamentoVazio = verificacaoPatrimonio.equipamentoVazio(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in equipamentoVazio])
    retorno.append({'desc':u'Patrimonios sem Equipamento', 'url':'patrimonio_equipamento_vazio', 'qtd':count})
    
    verificacaoPatrimonioEquipamento = VerificacaoPatrimonioEquipamento()
    partNumberDiferente = verificacaoPatrimonioEquipamento.partNumberDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in partNumberDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Part Number diferente', 'url':'patrimonio_equipamento_part_number_diferente', 'qtd':count})
    
    descricaoDiferente = verificacaoPatrimonioEquipamento.descricaoDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in descricaoDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Descricao diferente', 'url':'patrimonio_equipamento_descricao_diferente', 'qtd':count})

    marcaDiferente = verificacaoPatrimonioEquipamento.marcaDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in marcaDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Marca diferente', 'url':'patrimonio_equipamento_marca_diferente', 'qtd':count})

    modeloDiferente = verificacaoPatrimonioEquipamento.modeloDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in modeloDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Modelo diferente', 'url':'patrimonio_equipamento_modelo_diferente', 'qtd':count})

    ncmDiferente = verificacaoPatrimonioEquipamento.ncmDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in ncmDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com NCM diferente', 'url':'patrimonio_equipamento_ncm_diferente', 'qtd':count})
    
    tamanhoDiferente = verificacaoPatrimonioEquipamento.tamanhoDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in tamanhoDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Tamanho diferente', 'url':'patrimonio_equipamento_tamanho_diferente', 'qtd':count})
    
    tamanhoDiferente = verificacaoPatrimonio.procedenciaVazia(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in tamanhoDiferente])
    retorno.append({'desc':u'Patrimonio com procedecia vazia', 'url':'patrimonio_procedencia_vazia', 'qtd':count})
    
    retorno.append({'desc':u'Verificação de Patrimônios e Equipamentos', 'url':'check_patrimonio_equipamento', 'qtd':None})
    
    filtros = {"tipos":Tipo.objects.all()}
    
    return render_to_response('verificacao/patrimonio_consolidado.html', {'verificacoes':retorno, 'filtros':filtros}, context_instance=RequestContext(request))


@login_required
def patrimonio_procedencia_vazia(request):
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}
    
    retorno = []
    verficacao = VerificacaoPatrimonio()
    retorno = verficacao.procedenciaVazia(filtros_entrada)
    
    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":VerificacaoPatrimonioEquipamento().listaFiltroTipoPatrimonio(verficacao.equipamentoVazio()[0])}
    
    return render_to_response('verificacao/patrimonio_procedencia.html', 
                              {'desc':'Patrimonios sem Equipamento', 'patrimonios':retorno, 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_vazio(request):
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}
    
    retorno = []
    verficacao = VerificacaoPatrimonio()
    retorno = verficacao.equipamentoVazio(filtros_entrada)
    
    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":VerificacaoPatrimonioEquipamento().listaFiltroTipoPatrimonio(verficacao.equipamentoVazio()[0])}
    
    return render_to_response('verificacao/patrimonio.html', 
                              {'desc':'Patrimonios sem Equipamento', 'patrimonios':retorno, 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))

@login_required
def patrimonio_equipamento_part_number_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.partNumberDiferente(filtros_entrada)
    
    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":verficacao.listaFiltroTipoPatrimonio(verficacao.descricaoDiferente()[0])}
    
    if ajax:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Part Number diferente', 'patrimonios':retorno, 'atributo':'part_number', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Part Number diferente', 'patrimonios':retorno, 'atributo':'part_number', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_descricao_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.descricaoDiferente(filtros_entrada)
    
    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":verficacao.listaFiltroTipoPatrimonio(verficacao.descricaoDiferente()[0])}
    
    if ajax:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Descricao diferente', 'patrimonios':retorno, 'atributo':'descricao', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Descricao diferente', 'patrimonios':retorno, 'atributo':'descricao', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_marca_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.marcaDiferente(filtros_entrada)
    
    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":verficacao.listaFiltroTipoPatrimonio(verficacao.marcaDiferente()[0])}

    
    if ajax:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Marca diferente', 'patrimonios':retorno, 'atributo':'marca', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Marca diferente', 'patrimonios':retorno, 'atributo':'marca', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))



@login_required
def patrimonio_equipamento_modelo_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.modeloDiferente(filtros_entrada)
    

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":verficacao.listaFiltroTipoPatrimonio(verficacao.modeloDiferente()[0])}
    
    if ajax:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Modelo diferente', 'patrimonios':retorno, 'atributo':'modelo', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Modelo diferente', 'patrimonios':retorno, 'atributo':'modelo', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_ncm_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}
    
    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.ncmDiferente(filtros_entrada)
    

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":verficacao.listaFiltroTipoPatrimonio(verficacao.ncmDiferente()[0])}

    
    if ajax:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com NCM diferente', 'patrimonios':retorno, 'atributo':'ncm', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))
    else:    
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com NCM diferente', 'patrimonios':retorno, 'atributo':'ncm', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))



@login_required
def patrimonio_equipamento_tamanho_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio':request.GET.get('filtro_tipo_patrimonio')}
    
    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.tamanhoDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos":verficacao.listaFiltroTipoPatrimonio(verficacao.tamanhoDiferente()[0])}

    
    if ajax:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Tamanho diferente', 'patrimonios':retorno, 'atributo':'tamanho', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))
    else:    
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Tamanho diferente', 'patrimonios':retorno, 'atributo':'tamanho', 'filtros':filtros_saida}, 
                              context_instance=RequestContext(request))


@login_required
def copy_attribute_to_patrimonio(request):
    # Id do patrimonio
    patrimonio_id = request.GET.get('patrimonio_id')
    # Destino do valor a ser copiado ['patrimonio', 'equipamento']
    to_object = request.GET.get('to_object')
    # Nome do atributo a ser copiado
    att_name = request.GET.get('att_name')
    
    verficacao = VerificacaoPatrimonioEquipamento()
    verficacao.copy_attribute(to_object, patrimonio_id, att_name)
    if att_name == 'descricao':
        return patrimonio_equipamento_descricao_diferente(request)
    elif att_name == 'modelo':
        return patrimonio_equipamento_modelo_diferente(request)
    elif att_name == 'marca':
        return patrimonio_equipamento_marca_diferente(request)
    elif att_name == 'ncm':
        return patrimonio_equipamento_ncm_diferente(request)
    elif att_name == 'part_number':
        return patrimonio_equipamento_part_number_diferente(request)
    elif att_name == 'tamanho':
        return patrimonio_equipamento_tamanho_diferente(request)
    else:
        raise ValueError('Valor inválido para o parametro. att_name' + str(att_name))
    
    
