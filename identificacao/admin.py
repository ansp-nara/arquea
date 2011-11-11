# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.utils.translation import ugettext_lazy as _
from forms import *



class IdentificacaoInline(admin.TabularInline):
    model = Identificacao
    extra = 1

class EntidadeHistoricoInline(admin.TabularInline):
    model = EntidadeHistorico
    extra = 3

class ArquivoEntidadeInline(admin.TabularInline):
    model = ArquivoEntidade
    extra = 1

class AgendadoInline(admin.TabularInline):
    model = Agendado
    extra = 1

class EnderecoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'sigla' da entidade, 'nome' do contato  e
                         'rua', 'bairro', 'cidade', 'estado', e 'pais' do endereço.
    """

    fieldsets = (
                 (None, {
                     'fields': ('entidade',),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': (('rua', 'num'), ('compl', 'cep'), ('bairro', 'cidade'), ('estado', 'pais')),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('__unicode__', 'cep', 'bairro', 'cidade', 'estado', 'pais')

    search_fields = ['entidade__nome', 'entidade__sigla', 'identificacao__contato__nome', 'rua', 'bairro', 'cidade', 'estado', 'pais']

admin.site.register(Endereco, EnderecoAdmin)



class EnderecoInline(admin.StackedInline):
    fieldsets = (
                 (None, {
                     'fields': (('entidade' ), ('rua', 'num', 'compl'), ('cep', 'bairro', 'cidade'), ('estado', 'pais')),
                 }),
    )

    form = EnderecoAdminForm

    model = Endereco
    extra = 1



class ContatoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'email'.
    """

    fieldsets = (
                 (None, {
                     'fields': (('nome', 'ativo'), ('email', 'tel')),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('nome', 'contato_ent', 'email', 'tel', 'ativo')

    search_fields = ['nome', 'email']

    form = ContatoAdminForm

admin.site.register(Contato, ContatoAdmin)



class EntidadeAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'sigla' e 'nome'.
    """

    fieldsets = (
                 (None, {
                     'fields': (('entidade', 'sigla', 'nome'), ),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('url', ('cnpj', 'fisco'), 'pertence'),
                     'classes': ('wide',)
                 }),

    )

    list_display = ('sigla_nome','url', 'cnpj', 'fisco')

    list_filter = ('fisco', )

    inlines = [ArquivoEntidadeInline, EntidadeHistoricoInline, AgendadoInline]

    search_fields = ['sigla', 'nome']

admin.site.register(Entidade, EntidadeAdmin)



class IdentificacaoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'sigla' da entidade e
                         'nome', 'funcao' e 'area' do contato.
    """

    fieldsets = (
                 (None, {
                     'fields': (('endereco', 'contato', 'ativo'), ),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('funcao', 'area'),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('__unicode__', 'funcao', 'area', 'formata_historico')

    search_fields = ['endereco__entidade__nome', 'endereco__entidade__sigla', 'contato__nome', 'funcao', 'area']

admin.site.register(Identificacao, IdentificacaoAdmin)

class EnderecoDetalheAdmin(admin.ModelAdmin):
    form = EnderecoDetalheAdminForm

    fieldsets = (
                 (None, {
		    'fields': ('entidade', ('endereco', 'detalhe'), 'tipo', 'complemento'),
		    'classes': ('wide',)
		 }),
    )


admin.site.register(EnderecoDetalhe,EnderecoDetalheAdmin)
admin.site.register(TipoDetalhe)
admin.site.register(TipoEntidade)
admin.site.register(Agenda)
admin.site.register(TipoArquivoEntidade)
admin.site.register(Acesso)
admin.site.register(NivelAcesso)
admin.site.register(ASN)
