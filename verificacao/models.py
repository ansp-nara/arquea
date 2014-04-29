# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q, Max
import datetime

import logging
from django.db.models import F, Sum, Count
from patrimonio.models import Equipamento, Patrimonio, Tipo


# Get an instance of a logger
logger = logging.getLogger(__name__)


class VerificacaoEquipamento():

    equipamentos = []
    
    def marcaVazia(self):
        """
        Verifica o equipamento com marca/fabricante/editora vazia
        """
        
        retorno = []
        retorno = Equipamento.objects.filter(entidade_fabricante__isnull=True).order_by('entidade_fabricante__sigla')
        
        return retorno

    def partNumberVSModeloDiferente(self):
        """
        Verifica o equipamento pelo part_number
        buscando por modelos diferentes
        """

        retorno = []
        # busca por part_number que possuam mais que um equipamento cadastrado
        part_numbers = Equipamento.objects.exclude(part_number__exact='').values("part_number").annotate(qtd=Count("part_number")).order_by().filter(qtd__gt = 1)
        
        for pn_item in part_numbers:
            num_modelos = Equipamento.objects.filter(part_number=pn_item['part_number']).values("modelo").annotate(c=Count("modelo")).order_by().count()
            
            if num_modelos != 1:
                equipamentos = Equipamento.objects.filter(part_number=pn_item['part_number']).order_by("id")
                
                retorno.append(equipamentos)

        return retorno
    

    def partNumberVazio(self):
        """
        Verifica o equipamento pelo part_number
        que esteja vazio
        """

        # busca por part_number vazio
        retorno = []
        equipamentos = Equipamento.objects.filter(part_number='').order_by("id")
        
        retorno.append(equipamentos)

        return retorno
    
    def partNumberVazioModeloVazio(self):
        """
        Verifica o equipamento pelo part_number
        que esteja vazio
        """

        # busca por part_number vazio
        retorno = []
        equipamentos = Equipamento.objects.filter(part_number='').filter(modelo='').order_by("id")
        
        retorno.append(equipamentos)

        return retorno
    
    
class VerificacaoPatrimonio:

    def procedenciaVazia(self, filtros=None):
        """
        Verifica o patrimonio com procedencia vazia
        """
        
        retorno = []
        patrimonios = Patrimonio.objects.filter(entidade_procedencia__isnull=True).select_related("equipamento__entidade_fabricante").order_by("id")
        
        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)
        return retorno
    
    def equipamentoVazio(self, filtros=None):
        """
        Verifica patrimonio sem equipamento 
        """

        # busca por part_number vazio
        retorno = []
        patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=True).order_by("id")
        
        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)

        return retorno


    # busca de patrimonio cujos filhos estejam com historico_local diferente
    def localidadeDiferente(self, filtros=None):
        retorno = []
        
        patrimonios = Patrimonio.objects.filter(patrimonio__isnull=False)
        
        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        for p in patrimonios:
            # Busca patrimonios filhos que estão em localidade diferente deste patrimonio
            contido = self.localidadeDiferenteFilho(p, filtros)
            if len(contido) > 0:
                patrimonio = {}
                patrimonio.update({'id':p.id, 'modelo':p.modelo, 'descricao':p.descricao,
                                'endereco':'', 'estado':'', 'posicao':'', 'data':'', 'contido':[]})
                patrimonio.update({'endereco':p.historico_atual.endereco, 'estado':p.historico_atual.estado, 
                                   'posicao':p.historico_atual.posicao, 'data':p.historico_atual.data})
                patrimonio.update({'contido': contido})
                retorno.append(patrimonio)

        return retorno

    # busca de patrimonio cujos filhos estejam com historico_local diferente
    def localidadeDiferenteFilho(self, patrimonioPai, filtros=None):
        retorno = []
        
        if patrimonioPai and patrimonioPai.historico_atual:
            
            patrimonios = Patrimonio.objects.filter(patrimonio=patrimonioPai)
            
            if filtros and filtros["filtro_tipo_patrimonio"]:
                patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
            
            for p in patrimonios:
                if p.historico_atual:
                    # Verifica se a localidade do historico_atual é diferente do patrimonio pai
                    if patrimonioPai.historico_atual.endereco != p.historico_atual.endereco or \
                       patrimonioPai.historico_atual.posicao != p.historico_atual.posicao:
                    
                        patrimonio = {}
                        patrimonio.update({'id':p.id, 'modelo':p.modelo, 'descricao':p.descricao,
                                        'endereco':'', 'estado':'', 'posicao':'', 'data':'', 'contido':[]})
                        patrimonio.update({'endereco':p.historico_atual.endereco, 'estado':p.historico_atual.estado, 
                                           'posicao':p.historico_atual.posicao, 'data':p.historico_atual.data})

                        retorno.append(patrimonio)
        return retorno

    
class VerificacaoPatrimonioEquipamento():
    def listaFiltroTipoPatrimonio(self, patrimonios):
        pids = patrimonios.values_list('tipo_id', flat=True)
        tipos = Tipo.objects.filter(id__in=pids)
        
        return tipos
        
    
    # busca de patrimonio e equipamento
    # com part_number diferente
    def partNumberDiferente(self, filtros=None):
        retorno = []
        
        patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).filter(equipamento__part_number__isnull=False).exclude(equipamento__part_number=F('part_number')).select_related("equipamento").order_by("id")

        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)

        return retorno
    
    
    # busca de patrimonio e equipamento
    # com descrição diferente
    def descricaoDiferente(self, filtros=None):
        retorno = []

        patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).filter(equipamento__descricao__isnull=False).exclude(equipamento__descricao=F('descricao')).select_related("equipamento").order_by("id")

        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)
        return retorno
    
    
#     # busca de patrimonio e equipamento
#     # com marca diferente
#     def marcaDiferente(self, filtros=None):
#         retorno = []
#         
#         patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).filter(equipamento__entidade_fabricante__isnull=False).exclude(equipamento__entidade_fabricante__sigla=F('marca')).select_related("equipamento").order_by("id")
# 
#         if filtros and filtros["filtro_tipo_patrimonio"]:
#             patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
#         
#         retorno.append(patrimonios)
#         return retorno
    
     
    # busca de patrimonio e equipamento
    # com modelo diferente
    def modeloDiferente(self, filtros=None):
        retorno = []
        
        patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).filter(equipamento__modelo__isnull=False).exclude(equipamento__modelo=F('modelo')).select_related("equipamento").order_by("id")

        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)
        return retorno   
    
        
    # busca de patrimonio e equipamento
    # com ncm diferente
    def ncmDiferente(self, filtros=None):
        retorno = []
        
        patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).filter(equipamento__ncm__isnull=False).exclude(equipamento__ncm=F('ncm')).select_related("equipamento").order_by("id")

        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)
        return retorno
    
        
    # busca de patrimonio e equipamento
    # com tamanho em Us diferente
    def tamanhoDiferente(self, filtros=None):
        retorno = []
        
        patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).filter(equipamento__tamanho__isnull=False).exclude(equipamento__tamanho=F('tamanho')).select_related("equipamento").order_by("id")

        if filtros and filtros["filtro_tipo_patrimonio"]:
            patrimonios = patrimonios.filter(tipo=filtros["filtro_tipo_patrimonio"])
        
        retorno.append(patrimonios)
        return retorno


    def copy_attribute(self, to_object, patrimonio_id, att_name):
        """
        to_object = ['patrimonio', 'equipamento']   objeto a ser copiado. deve ser de equipamento para patrimonio, ou de patrimonio para equipamento
        patrimonio_id = id do patrimonio
        att_name = nome do atributo do objeto
        """
        
        if to_object == 'patrimonio':
            patr = Patrimonio.objects.get(id=patrimonio_id)
            eq = Equipamento.objects.get(id=patr.equipamento.id)
            
            if att_name == 'descricao':
                 patr.descricao = eq.descricao
                 patr.save()
            elif att_name == 'modelo':
                patr.modelo = eq.modelo
                patr.save()
            elif att_name == 'marca':
                patr.marca = eq.marca
                patr.save()
            elif att_name == 'ncm':
                patr.ncm = eq.ncm
                patr.save()
            elif att_name == 'part_number':
                patr.part_number = eq.part_number
                patr.save()
            elif att_name == 'procedencia':
                patr.entidade_procedencia_id = eq.entidade_fabricante_id
                patr.save()
            else:
                raise ValueError('Valor inválido para o parametro. att_name' + str(att_name))        
            
        elif to_object == 'equipamento':
            patr = Patrimonio.objects.get(id=patrimonio_id)
            eq = Equipamento.objects.get(id=patr.equipamento.id)
            
            if att_name == 'descricao':
                eq.descricao = patr.descricao
                eq.save()
            elif att_name == 'modelo':
                eq.modelo = patr.modelo
                eq.save()
            elif att_name == 'marca':
                eq.marca = patr.marca
                eq.save()
            elif att_name == 'ncm':
                eq.ncm = patr.ncm
                eq.save()
            elif att_name == 'part_number':
                eq.part_number = patr.part_number
                eq.save()
            else:
                raise ValueError('Valor inválido para o parametro. att_name' + str(att_name))
            
            
        else:
            raise ValueError('Valor inválido para o parametro. to_object=' + str(to_object))        
        
        
        
        