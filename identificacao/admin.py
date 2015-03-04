# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
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

class EnderecoDetalheInline(admin.TabularInline):
    model = EnderecoDetalhe
    extra = 1

class ASNInline(admin.TabularInline):
    model = ASN
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
                     'fields': (('rua', 'num'), ('compl', 'cep'), ('bairro', 'cidade'), ('estado', 'pais'), 'data_inatividade'),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('__unicode__', 'cep', 'bairro', 'cidade', 'estado', 'pais')

    search_fields = ['entidade__nome', 'entidade__sigla', 'identificacao__contato__primeiro_nome', 'identificacao__contato__ultimo_nome', 'rua', 'bairro', 'cidade', 'estado', 'pais']
    inlines = [EnderecoDetalheInline]

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
                     'fields': (('primeiro_nome', 'ultimo_nome', 'ativo'), ('email', 'tel', 'documento')),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('nome', 'contato_ent', 'email', 'tel', 'ativo')

    search_fields = ['primeiro_nome', 'ultimo_nome', 'email']

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
                     'fields': ('url', ('cnpj', 'fisco'), ('recebe_doacao',)),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('sigla_nome', 'sigla_completa', 'url', 'cnpj', 'fisco', 'recebe_doacao')

    list_filter = ('fisco', )

    inlines = [ArquivoEntidadeInline, ASNInline, EntidadeHistoricoInline, AgendadoInline]

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

    search_fields = ['endereco__entidade__nome', 'endereco__entidade__sigla', 'contato__primeiro_nome', 'contato__ultimo_nome', 'funcao', 'area']

admin.site.register(Identificacao, IdentificacaoAdmin)



class EnderecoDetalheEntidadeFilter(SimpleListFilter):
    title = 'Entidade'
    parameter_name = 'endereco__entidade__sigla'

    def lookups(self, request, model_admin):
        entidade_ids = EnderecoDetalhe.objects.values_list('endereco__entidade_id', flat=True).distinct().order_by()
        return [(e.id, e.sigla) for e in Entidade.objects.filter(id__in=entidade_ids)]

    def queryset(self, request, queryset):
        id=self.value()
        if id:
            return queryset.filter(endereco__entidade__id__exact=id) | \
                   queryset.filter(detalhe__endereco__entidade__id__exact=id)
        else: return queryset

    
class EnderecoDetalheAdmin(admin.ModelAdmin):
    form = EnderecoDetalheAdminForm

    fieldsets = (
                 (None, {
		    'fields': ('entidade', ('endereco', 'detalhe'), 'tipo', 'complemento'),
		    'classes': ('wide',)
		 }),
    )

    search_fields = ['', 'endereco__rua', 'detalhe__endereco__entidade__sigla']
    
    list_filter = (EnderecoDetalheEntidadeFilter, 'tipo')

class ASNAdmin(admin.ModelAdmin):

    list_display = ('numero', 'entidade', 'pais')
    search_fields = ('entidade__sigla', 'numero')


admin.site.register(EnderecoDetalhe,EnderecoDetalheAdmin)
admin.site.register(TipoDetalhe)
admin.site.register(TipoEntidade)
admin.site.register(Agenda)
admin.site.register(TipoArquivoEntidade)
admin.site.register(Acesso)
admin.site.register(NivelAcesso)
admin.site.register(ASN, ASNAdmin)
admin.site.register(Ecossistema)
