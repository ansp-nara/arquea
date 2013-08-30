# -* coding: utf-8 -*-

# Create your views here.

from decimal import Decimal
from django.contrib import admin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Max, Sum, Count 
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from models import *
from verificacao.models import VerificacaoEquipamento
from operator import itemgetter
from utils.functions import pega_lista, formata_moeda, render_to_pdf
import cStringIO as StringIO
import cgi
import datetime
import ho.pisa as pisa
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
        
    verificacaoPatrimonio = VerificacaoPatrimonio()
    equipamentoVazio = verificacaoPatrimonio.equipamentoVazio()
    count = sum([len(patrimonios) for patrimonios in equipamentoVazio])
    retorno.append({'desc':u'Patrimonios sem Equipamento', 'url':'patrimonio_equipamento_vazio', 'qtd':count})
    
    verificacaoPatrimonio = VerificacaoPatrimonioEquipamento()
    partNumberDiferente = verificacaoPatrimonio.partNumberDiferente()
    count = sum([len(patrimonios) for patrimonios in partNumberDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Part Number diferente', 'url':'patrimonio_equipamento_part_number_diferente', 'qtd':count})
    
    verificacaoPatrimonio = VerificacaoPatrimonioEquipamento()
    descricaoDiferente = verificacaoPatrimonio.descricaoDiferente()
    count = sum([len(patrimonios) for patrimonios in descricaoDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Descricao diferente', 'url':'patrimonio_equipamento_descricao_diferente', 'qtd':count})

    verificacaoPatrimonio = VerificacaoPatrimonioEquipamento()
    marcaDiferente = verificacaoPatrimonio.marcaDiferente()
    count = sum([len(patrimonios) for patrimonios in marcaDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Marca diferente', 'url':'patrimonio_equipamento_marca_diferente', 'qtd':count})

    verificacaoPatrimonio = VerificacaoPatrimonioEquipamento()
    modeloDiferente = verificacaoPatrimonio.modeloDiferente()
    count = sum([len(patrimonios) for patrimonios in modeloDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com Modelo diferente', 'url':'patrimonio_equipamento_modelo_diferente', 'qtd':count})

    verificacaoPatrimonio = VerificacaoPatrimonioEquipamento()
    ncmDiferente = verificacaoPatrimonio.ncmDiferente()
    count = sum([len(patrimonios) for patrimonios in ncmDiferente])
    retorno.append({'desc':u'Patrimonio e Equipamento com NCM diferente', 'url':'patrimonio_equipamento_ncm_diferente', 'qtd':count})
    
    
    return render_to_response('verificacao/patrimonio_consolidado.html', {'verificacoes':retorno}, context_instance=RequestContext(request))

@login_required
def patrimonio_equipamento_vazio(request):

    retorno = []
    verficacao = VerificacaoPatrimonio()
    retorno = verficacao.equipamentoVazio()
    
    return render_to_response('verificacao/patrimonio.html', 
                              {'desc':'Patrimonios sem Equipamento', 'patrimonios':retorno}, 
                              context_instance=RequestContext(request))

@login_required
def patrimonio_equipamento_part_number_diferente(request):
    json = request.GET.get('json')

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.partNumberDiferente()
    
    if json:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Part Number diferente', 'patrimonios':retorno, 'atributo':'part_number'}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Part Number diferente', 'patrimonios':retorno, 'atributo':'part_number'}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_descricao_diferente(request):
    json = request.GET.get('json')

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.descricaoDiferente()
    
    if json:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Descricao diferente', 'patrimonios':retorno, 'atributo':'descricao'}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Descricao diferente', 'patrimonios':retorno, 'atributo':'descricao'}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_marca_diferente(request):
    json = request.GET.get('json')
    
    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.marcaDiferente()
    
    if json:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Marca diferente', 'patrimonios':retorno, 'atributo':'marca'}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Marca diferente', 'patrimonios':retorno, 'atributo':'marca'}, 
                              context_instance=RequestContext(request))



@login_required
def patrimonio_equipamento_modelo_diferente(request):
    json = request.GET.get('json')
    
    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.modeloDiferente()
    
    if json:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com Modelo diferente', 'patrimonios':retorno, 'atributo':'modelo'}, 
                              context_instance=RequestContext(request))
    else:
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com Modelo diferente', 'patrimonios':retorno, 'atributo':'modelo'}, 
                              context_instance=RequestContext(request))


@login_required
def patrimonio_equipamento_ncm_diferente(request):
    json = request.GET.get('json')

    retorno = []
    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.ncmDiferente()

    if json:
        return render_to_response('verificacao/patrimonio_equipamento-table.html', 
                              {'desc':'Patrimonio e Equipamento com NCM diferente', 'patrimonios':retorno, 'atributo':'ncm'}, 
                              context_instance=RequestContext(request))
    else:    
        return render_to_response('verificacao/patrimonio_equipamento.html', 
                              {'desc':'Patrimonio e Equipamento com NCM diferente', 'patrimonios':retorno, 'atributo':'ncm'}, 
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
    else:
        raise ValueError('Valor inválido para o parametro. att_name' + str(att_name))
    
    
    
def copy_attribute_to_equipamento(request):
    # Id do equipamento
    eq_id = request.GET.get('eq_id')


