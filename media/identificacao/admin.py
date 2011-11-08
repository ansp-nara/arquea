# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Entidade, Identificacao, Contato, Endereco
from django.utils.translation import ugettext_lazy as _
from forms import ContatoAdminForm, EnderecoAdminForm



class IdentificacaoInline(admin.TabularInline):
    model = Identificacao
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
                     'fields': (('sigla', 'nome', 'ativo'), ),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('url', ('cnpj', 'fisco'), 'asn'),
                     'classes': ('wide',)
                 }),

    )

    list_display = ('sigla_nome','url', 'cnpj', 'ativo', 'fisco')

    list_filter = ('ativo','fisco')

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
