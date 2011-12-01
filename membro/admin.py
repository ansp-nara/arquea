# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.utils.translation import ugettext_lazy as _
from forms import *



admin.site.register(TipoAssinatura)


class HistoricoInline(admin.TabularInline):
    model = Historico
    extra = 1

class MembroAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome', 'rg', 'cpf', 'cargo' e 'email' do membro.
    """

    fieldsets = (
                 (None, {
                     'fields': ('nome', ('email', 'ramal'), ('foto', 'site') ),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('data_nascimento', ('rg', 'cpf'), 'url_lattes' ),
                     'classes': ('wide',)
                 }),
                 ('Observação', {
                     'fields': ('obs', ),
                     'classes': ('collapse',)
                 }),
    )

    list_display = ('nome', 'cargo_atual', 'email', 'existe_ramal', 'existe_curriculo')

    list_display_links = ('nome', )

    form = MembroAdminForm
    inlines = [HistoricoInline]

    list_per_page = 10

    search_fields = ['nome', 'rg', 'cpf', 'email']

admin.site.register(Membro, MembroAdmin)



class AssinaturaAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'tipo' de assinatura e,
                         'nome' e 'cargo' do membro.
    """

    fieldsets = (
                 (None, {
                     'fields': (('membro', 'tipo_assinatura'), ),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('membro', 'tipo_assinatura')

    list_per_page = 10

    search_fields = ['tipo_assinatura__nome', 'membro__nome']

admin.site.register(Assinatura, AssinaturaAdmin)


class ControleFeriasInline(admin.TabularInline):
    model = ControleFerias
    form = ControleFeriasAdminForm
    formset = ControleFeriasAdminFormSet
    extra = 0

class FeriasAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'cargo' do membro, 
                         'inicio' e 'termino' de férias.
    """

    fieldsets = (
                 (None, {
                     'fields': ('membro', ),
                     'classes': ('wide',)
                 }),
                 ('Período de Trabalho', {
                     'fields': (('inicio', 'realizado'), 'decimo_terceiro'),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('membro', 'inicio', 'completo', 'realizado')
    #form = FeriasAdminForm
    inlines = [ControleFeriasInline, ]
    list_per_page = 10

    search_fields = ['membro__nome', 'membro__cargo']

admin.site.register(Ferias, FeriasAdmin)



class DadoBancarioAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' do contato,
                         'banco', 'agencia' e 'cc' do modelo DadoBancario.
    """

    fieldsets = (
                 (None, {
                     'fields': ('membro', ),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('banco', ('agencia', 'ag_digito', 'conta', 'cc_digito')),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('membro', 'banco', 'agencia_digito', 'conta_digito')

#    form = DadoBancarioAdminForm

    search_fields = ['membro__nome', 'banco', 'agencia', 'cc']

admin.site.register(DadoBancario, DadoBancarioAdmin)

admin.site.register(Cargo)
admin.site.register(TipoDispensa)

class DispensaLegalAdmin(admin.ModelAdmin):

    fieldsets = (
                 (None, {
                     'fields': (('membro', 'tipo'), ('inicio_direito', 'dias_uteis'), 'justificativa')
                 }),
                 (None, {
                     'fields': (('inicio_realizada', 'realizada'), ('atestado', 'arquivo'))
                 }),
    )
    list_display = ('membro', 'tipo', 'inicio_direito', 'realizada')

admin.site.register(DispensaLegal, DispensaLegalAdmin)
