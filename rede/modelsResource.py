#-*- encoding:utf-8 -*-
from import_export import fields
from import_export import resources
from rede.models import *
from utils.functions import formata_moeda


"""
Modelo do model Recurso para a geração do XLS para o relatório Custo Terremark
"""
class CustoTerremarkRecursoResource(resources.ModelResource):
    total_sem_imposto = fields.Field(column_name='Total sem imposto')
    total_geral = fields.Field(column_name='Total com imposto')
    planejamento__valor_unitario = fields.Field(column_name='Preço unitário')
    planejamento__os__contrato__numero = fields.Field(column_name='Contrato')
    planejamento__os = fields.Field(column_name='OS')
    planejamento__os__data_inicio = fields.Field(column_name='Data')
    planejamento__tipo = fields.Field(column_name='Descrição')
    planejamento__referente = fields.Field(column_name='Referente')
    planejamento__unidade = fields.Field(column_name='Unidade')
    planejamento__quantidade = fields.Field(column_name='Qtd')
    valor_mensal_sem_imposto = fields.Field(column_name='Custo mensal sem imposto')
    valor_imposto_mensal = fields.Field(column_name='Custo mensal com imposto')
    quantidade = fields.Field(column_name='Meses pagos')
    pagamento__protocolo__num_documento = fields.Field(column_name='Nota fiscal')

    class Meta:
        model = Recurso
        fields = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__os__data_inicio',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__unidade',
                  'planejamento__valor_unitario',
                  'planejamento__quantidade',
                  'valor_mensal_sem_imposto',
                  'valor_imposto_mensal',
                  'quantidade',
                  'total_sem_imposto',
                  'total_geral',
                  'pagamento__protocolo__num_documento'
                  )
        export_order = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__os__data_inicio',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__unidade',
                  'planejamento__valor_unitario',
                  'planejamento__quantidade',
                  'valor_mensal_sem_imposto',
                  'valor_imposto_mensal',
                  'quantidade',
                  'total_sem_imposto',
                  'total_geral',
                  'pagamento__protocolo__num_documento'
                  )

    def dehydrate_total_sem_imposto(self, recurso):
        return recurso.total_sem_imposto()
    def dehydrate_total_geral(self, recurso):
        return recurso.total_geral()
    def dehydrate_planejamento__valor_unitario(self, recurso):
        return recurso.planejamento.valor_unitario
    def dehydrate_planejamento__os__contrato__numero(self, recurso):
        return '%s' % recurso.planejamento.os.contrato.numero
    def dehydrate_planejamento__os(self, recurso):
        return '%s' % recurso.planejamento.os
    def dehydrate_planejamento__os__data_inicio(self, recurso):
        return '%s' % recurso.planejamento.os.data_inicio
    def dehydrate_planejamento__tipo(self, recurso):
        return '%s' % recurso.planejamento.tipo
    def dehydrate_planejamento__referente(self, recurso):
        return '%s' % recurso.planejamento.referente
    def dehydrate_planejamento__unidade(self, recurso):
        return '%s' % recurso.planejamento.unidade
    def dehydrate_planejamento__quantidade(self, recurso):
        return recurso.planejamento.quantidade
    def dehydrate_valor_mensal_sem_imposto(self, recurso):
        return recurso.valor_mensal_sem_imposto
    def dehydrate_valor_imposto_mensal(self, recurso):
        return recurso.valor_imposto_mensal
    def dehydrate_quantidade(self, recurso):
        return recurso.quantidade
    def dehydrate_pagamento__protocolo__num_documento(self, recurso):
        return '%s' % recurso.pagamento.protocolo.num_documento
