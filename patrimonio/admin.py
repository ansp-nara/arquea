# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.utils.translation import ugettext_lazy as _
from forms import *
from django.utils.encoding import smart_unicode



admin.site.register(Estado)
admin.site.register(Tipo)

class HistoricoLocalInline(admin.StackedInline):
    fieldsets = (('', {
                   'fields':(('entidade'), ('endereco',), ('descricao', 'data', 'estado', 'memorando'))
                }),)
    model = HistoricoLocal
    form = HistoricoLocalAdminForm
    choices = 1

class PatrimonioAdmin(admin.ModelAdmin):
 
    fieldsets = (
                 ('Pagamento', {
		      'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
                      'classes': ('wide',)
                 }),
	         ('Geral', {
		      'fields': ('tipo', ('part_number', 'ns'), 'patrimonio', 'descricao', ('marca', 'modelo', 'procedencia'))
                 }),
 	         ('Extras', {
		      'fields': ('imagem', 'obs', 'titulo_autor', 'isbn'),
		      'classes': ('collapse',)
                 }),
    )

    form = PatrimonioAdminForm
    list_display = ('tipo', 'descricao', 'marca', 'ns', 'nf')
    list_filter = ('tipo', 'pagamento__protocolo__termo',)
    inlines = [HistoricoLocalInline,]
    search_fields = ('descricao', 'ns')

admin.site.register(Patrimonio,PatrimonioAdmin)

class HistoricoLocalAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'sigla' da entidade,
                         'nome' do contato,
                         'funcao' e 'area' da identificacao,
                         'rua', 'complemento', 'bairro', 'cidade', 'cep', 'estado' e 'pais' do endereço,
                         'descricao' do item do protocolo,
                         'número do documento' e 'descricao' do protocolo e,
                         'descricao' e 'data' do histórico.
    """

    fieldsets = (
                 (None, {
                     'fields': ('data', 'patrimonio', 'endereco', 'descricao'),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('data', 'patrimonio', 'endereco', 'descricao')

    search_fields = ['endereco__identificacao____entidade__nome', 'endereco__identificacao__entidade__sigla', 'endereco__identificacao__contato__nome', 'endereco__identificacao__funcao', 'endereco__identificacao__area', 'endereco__rua', 'endereco__complemento', 'endereco__bairro', 'endereco__cidade', 'endereco__estado', 'endereco__cep', 'endereco__pais', 'descrica', 'data', 'patrimonio__itemprotocolo__descricao', 'patrimonio__itemprotocolo__protocolo__num_documento', 'patrimonio__itemprotocolo__protocolo__descricao']

admin.site.register(HistoricoLocal, HistoricoLocalAdmin)

