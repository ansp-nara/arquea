# -*- coding: utf-8 -*-

from django.contrib import admin
from models import OrdemDeServico, Contrato, Termo, Outorga, Modalidade, Estado, Natureza_gasto, Item, Categoria, Arquivo, Acordo, OrigemFapesp, ArquivoOS, TipoContrato
from forms import *
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from identificacao.models import Entidade
from rede.models import PlanejaAquisicaoRecurso

class Natureza_gastoInline(admin.TabularInline):
    model = Natureza_gasto
    extra = 6


class PlanejamentoInline(admin.StackedInline):
    model = PlanejaAquisicaoRecurso
    extra = 2
    fieldsets = (
                 (None, {
                         'fields': (('os', 'ano'), ('tipo', 'referente'), ('quantidade', 'valor_unitario'), ('projeto', 'unidade', 'instalacao'), 'obs'),
                         'classes': ('wide',)
                        }
                 ),
                )

class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 2
    verbose_name = ''
    verbose_name_plural = 'Arquivos'


class ArquivoOSInline(admin.TabularInline):
    model = ArquivoOS
    extra = 2
    verbose_name = ''
    verbose_name_plural = 'Arquivos'

class ItemInline(admin.StackedInline):
    fieldsets = (
                 (None, {
                     'fields': ('natureza_gasto', ('descricao', 'entidade', 'quantidade'), 'valor'),
                 }),
                 (_(u'Justificativa/Observação'), {
                     'fields': ('justificativa', 'obs',),
                     'classes': ('collapse',)
                 }),
    )

    model = Item
    form = ItemAdminForm
    extra = 3
    verbose_name = ''
    verbose_name_plural = 'Itens'



class OutorgaInline(admin.StackedInline):
    fieldsets = (
                 (None, {
                     'fields': (('data_solicitacao', 'termino', 'data_presta_contas', 'categoria'), ('arquivo', 'protocolo')),
                 }),
                 ('Observação', {
                     'fields': ('obs', ),
                     'classes': ('collapse', ),
                 }),
    )

    model = Outorga
    extra = 1
    ordering = ('-data_solicitacao',)

class OrigemFapespInline(admin.TabularInline):
    model = OrigemFapesp
    extra = 2
    ordering = ('item_outorga__natureza_gasto__termo', 'item_outorga__descricao')
    form = OrigemFapespForm

class OrigemFapespInlineA(OrigemFapespInline):
    fields = ('termo', 'item_outorga')
    readonly_fields = ('termo',)

class OrdemDeServicoInline(admin.StackedInline):

    fieldsets = (
                (None, {
                    'fields': ('acordo', ('tipo', 'numero'), ('data_inicio', 'data_rescisao', 'antes_rescisao'))
                 }),
                 (_(u'Descrição'), {
                     'fields': ('descricao', ),
                     'classes': ('collapse', ),
                 }),
    )

    model = OrdemDeServico
    extra = 0
    verbose_name = ''
    verbose_name_plural = 'Alteração de contratos'


class AcordoAdmin(admin.ModelAdmin):
    """
    Permite busca por	'nome' do Estado,
			'descrição' do Acordo.
    """

    list_display = ('descricao', 'estado', )
    search_fields = ('descricao', 'estado__nome', )
    list_per_page = 10
    inlines = [OrigemFapespInlineA]

admin.site.register(Acordo,AcordoAdmin)


                
class EstadoAdmin(admin.ModelAdmin):

    """
    Permite consulta por:	'nome' do Estado.
    """

    fieldsets = (
                 (None, {
                     'fields': ('nome', ),
                 }),
    )

    list_display = ('nome', )

    search_fields = ('nome', )

    list_per_page = 10

admin.site.register(Estado, EstadoAdmin)



class CategoriaAdmin(admin.ModelAdmin):

    """
    Permite consulta por:	'nome' da Categoria.
    """

    fieldsets = (
                 (None, {
                     'fields': ('nome', ),
                 }),
    )

    list_display = ('nome', )

    search_fields = ('nome', )

    list_per_page = 10

admin.site.register(Categoria, CategoriaAdmin)



class ModalidadeAdmin(admin.ModelAdmin):

    """
    Permite consulta por:	'sigla' e 'nome' da Modalidade.
    """

    fieldsets = (
                 (None, {
                     'fields': (('sigla', 'nome', 'moeda_nacional'), ),
                 }),
    )

    list_display = ('sigla', 'nome', 'moeda_nacional')

    list_display_links = ('sigla', 'nome', )

    search_fields = ('sigla', 'nome')

    list_per_page = 10

admin.site.register(Modalidade, ModalidadeAdmin)



class TermoAdmin(admin.ModelAdmin):

    """
    Permite consulta por:	'ano' e 'processo' do Termo,
				'nome' do Outorgado,
				'data_concessao' do Termo.
    """

    fieldsets = (
                 (None, {
                     'fields': (('ano', 'processo', 'digito', 'inicio', 'estado'), \
                                'parecer', 'parecer_final', 'projeto', 'orcamento', 'extrato_financeiro', 'quitacao', 'doacao', 'relatorio_final', 'exibe_rel_ger_progressivo'),
                 }),
    )

    #list_display = ('__unicode__', 'inicio', 'duracao_meses', 'termo_real', 'termo_dolar', 'formata_realizado_dolar', 'estado')

    list_display = ('__unicode__', 'inicio', 'duracao_meses', 'termo_real', 'formata_realizado_real', 'formata_saldo_real', 'termo_dolar', 'formata_realizado_dolar', 'formata_saldo_dolar', 'estado')
    inlines = (OutorgaInline, Natureza_gastoInline)

    search_fields = ('ano', 'processo', 'inicio')

    list_per_page = 10

admin.site.register(Termo, TermoAdmin)



class OutorgaAdmin(admin.ModelAdmin):

    """
    O método 'save_model'	Verifica se oo estado atual é diferente do estado anterior.
    O método 'response_change'	Encaminha o usuário para a tela de edição do termo se o estado for definido como 'Aprovado'.

    Filtra os dados por 'termo' e 'estado'.

    Permite consulta pelos campos: 	'nome' da Categoria,
                                        'ano', 'processo' e 'data_concessao' do Termo.
    """

    fieldsets = (
                 (None, {
                     'fields': (('data_solicitacao', 'termino', 'termo', 'data_presta_contas', 'categoria', 'arquivo'), ),
                 }),

                 ('Observação', {
                     'fields': ('obs', ),
                     'classes': ('collapse', ),
                 }),
    )

    list_display = ('data_solicitacao', 'inicio', 'termino', 'mostra_termo', 'data_presta_contas', 'mostra_categoria', 'arquivo')

    list_display_links = ('mostra_categoria', )

    search_fields = ('termo__ano', 'termo__processo', 'categoria__nome', 'data_presta_contas', 'data_solicitacao', 'termino')

    list_filter = ('termo', )

    list_per_page = 10

admin.site.register(Outorga, OutorgaAdmin)



class Natureza_gastoAdmin(admin.ModelAdmin):

    """
    Filtra os dados pelo pedido e pela modalidade.

    Permite consulta pelos campos:	'sigla' e 'nome' da Modalidade,
                                  	'categoria' do Pedido de Concessão,
                                  	'ano' e 'processo' do Termo.
    """

    fieldsets = (
                 (None, {
                     'fields': (('termo', 'modalidade'), 'valor_concedido' ),
                 }),
                 (_(u'Observação'), {
                     'fields': ('obs', ),
                     'classes': ('collapse',)
                 }),
    )

    list_display = ('termo', 'mostra_modalidade', 'v_concedido', 'formata_total_realizado', 'saldo')

    list_display_links = ('termo', 'mostra_modalidade', )

    search_fields = ('modalidade__sigla', 'modalidade__nome',  'termo__ano', 'termo__processo')

    list_filter = ('termo', 'modalidade')

    list_per_page = 10

admin.site.register(Natureza_gasto, Natureza_gastoAdmin)



class ItemAdmin(admin.ModelAdmin):

    """
    Filtra os dados por estado e pela natureza do gasto.

    Permite consulta pelos campos: 	'sigla' e 'nome' da Modalidade,
                                   	'nome' da Categoria do Pedido de Concessão,
                                   	'ano' e 'processo' do Termo,
                                   	'estado', 'descricao' e 'justificativa' do Item do Pedido de Concessão.
    """

    fieldsets = (
                 (None, {
                     'fields': (('termo', 'natureza_gasto'), ('descricao', 'entidade', 'quantidade'), 'valor'),
                 }),
                 (_(u'Justificativa/Observação'), {
                     'fields': ('justificativa', 'obs',),
                 }),
    )

    list_display = ('mostra_termo', 'mostra_modalidade', 'mostra_descricao', 'entidade', 'mostra_quantidade', 'mostra_valor_realizado', 'pagamentos_pagina')


    search_fields = ('natureza_gasto__modalidade__sigla', 'natureza_gasto__modalidade__nome', 'natureza_gasto__termo__ano', 'natureza_gasto__termo__processo', 'descricao', 'justificativa', 'obs')

    list_filter = ('natureza_gasto__termo', 'natureza_gasto__modalidade') 

    inlines = [OrigemFapespInline]
    form = ItemAdminForm
    
    list_display_links = ('mostra_descricao', )

    list_per_page = 20

admin.site.register(Item, ItemAdmin)



class ArquivoAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelo id do protocolo.
    Busca arquivo por: 	'ano' e 'processo' do Termo,
         		'nome' da Categoria e
                       	'arquivo' 
    """

    fieldsets = (
                (None, {
                    'fields': ('outorga', 'arquivo')
                 }),
    )

    list_display = ('mostra_termo', 'concessao', '__unicode__')

    list_display_links = ('__unicode__', )

    search_fields = ('outorga__termo__ano', 'outorga__termo__processo', 'outorga__categoria__nome', 'arquivo', )

    list_per_page = 10

admin.site.register(Arquivo,ArquivoAdmin)



class ContratoAdmin(admin.ModelAdmin):
    """
    """

    fieldsets = (
                (_(u'Contrato'), {
                    'fields': ('anterior', 'numero', ('data_inicio', 'limite_rescisao', 'entidade', 'auto_renova', 'arquivo'),)
                 }),
    )

    list_display = ('numero', 'data_inicio', 'limite_rescisao', 'entidade', 'auto_renova', 'existe_arquivo')

    list_display_links = ('entidade', )

    search_fields = ('entidade__sigla', 'entidade__nome', 'data_inicio' )

    inlines = (OrdemDeServicoInline, )

    list_per_page = 10

admin.site.register(Contrato,ContratoAdmin)



class OrdemDeServicoAdmin(admin.ModelAdmin):
    """
    """

    fieldsets = (
                (None, {
                    'fields': ('acordo', 'tipo')
                 }),
                (_(u'Ordem de Serviço'), {
                    'fields': ('numero', ('data_inicio', 'data_rescisao', 'contrato', 'antes_rescisao'), 'descricao', 'pergunta')
                 }),
    )

    list_display = ('numero', 'tipo', 'entidade', 'data_inicio', 'data_rescisao', 'mostra_prazo', 'descricao')

    list_display_links = ('descricao', )

    inlines = (ArquivoOSInline, PlanejamentoInline)

    search_fields = ('numero', 'acordo__descricao', 'contrato__entidade__sigla', 'contrato__entidade__nome', 'descricao', 'data_inicio', 'data_rescisao', 'tipo__nome')

    list_per_page = 10
    filter_horizontal = ('pergunta',)

admin.site.register(OrdemDeServico,OrdemDeServicoAdmin)
#admin.site.register(ArquivoOS)
admin.site.register(TipoContrato)
admin.site.register(OrigemFapesp)
