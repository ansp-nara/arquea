# -* coding: utf-8 -*-

# Create your views here.

from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q, Max, Sum, Count 
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

from models import *
from verificacao.models import VerificacaoEquipamento
from patrimonio.models import Tipo
import datetime
import json as simplejson
import os


import logging
from patrimonio.models import Equipamento
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
    
    return render_to_response('verificacao/equipamento_consolidado.html', {'verificacoes':retorno}, context_instance=RequestContext(request))

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
    
    filtros = {"tipos":Tipo.objects.all()}
    
    return render_to_response('verificacao/patrimonio_consolidado.html', {'verificacoes':retorno, 'filtros':filtros}, context_instance=RequestContext(request))

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
    
    logger.debug(filtros_entrada)
    
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
    
    logger.debug(filtros_entrada)
    
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
    
    
