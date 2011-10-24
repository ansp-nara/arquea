# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Patrimonio, Licenca, Publicacao, Equipamento, MonitoramentoInterno, Estado, Tipo, HistoricoLocal 
from django.utils.translation import ugettext_lazy as _
from forms import *
from django.contrib.admin.filterspecs import FilterSpec
from django.utils.encoding import smart_unicode
from outorga.models import Termo


class Filtros(FilterSpec):
    def has_output(self):
        return len(self.lookup_choices) > 1

    def title(self):
        return self.f_title

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
              'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
              'display': _('All')}
        for pk_val, val in self.lookup_choices:
            yield {'selected': self.lookup_val == smart_unicode(pk_val),
                  'query_string': cl.get_query_string({self.lookup_kwarg: pk_val}),
                  'display': val}



class Termos(Filtros):
    def __init__(self, request, params, model, model_admin):
        super(Termos, self).__init__(request, params, model, model_admin)
        self.lookup_kwarg = 'pagamento__protocolo__termo__id__exact'
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        self.lookup_choices = [(t.id, t.__unicode__()) for t in Termo.objects.all()]
        self.f_title = 'Termo de outorga'

admin.site.register(Estado)
admin.site.register(Tipo)

class HistoricoLocalInline(admin.StackedInline):
    fieldsets = (('', {
                   'fields':(('entidade'), ('endereco',), ('descricao', 'data', 'estado'))
		}),)
    model = HistoricoLocal
    form = HistoricoLocalAdminForm
    choices = 1

class LicencaAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'ano' e 'processo' do protocolo,
                         'nome' do estado,
                         'nome' do tipo,
                         'obs' e 'nome' da licença.
    """

    fieldsets = (

                 ('Protocolo', {
                     'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
                     'classes': ('wide',)
                 }),
                 ('Licença', {
                     'fields': (('nome', 'tipo'), 'qtde_usuarios' ),
                     'classes': ('wide',)
                 }),
                 ('Observação', {
                     'fields': ('obs', ),
                     'classes': ('collapse',)
                 }),
    )

    list_display = ('nome', 'mostra_tipo', 'qtde_usuarios')

    form = LicencaAdminForm


    list_per_page = 10

    search_fields = ('obs', 'nome', 'tipo__nome')

admin.site.register(Licenca, LicencaAdmin)



class PublicacaoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'ano' e 'processo' do protocolo,
                         'nome' do estado,
                         'obs', 'isbn', 'titulo', 'autor' e 'editora' da uublicacao.
    """

    fieldsets = (
                 ('Protocolo', {
                     'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
                     'classes': ('wide',)
                 }),
                 ('Publicação', {
                     'fields': (('autor', 'titulo'), ('editora', 'isbn') ),
                     'classes': ('wide',)
                 }),
                 ('Observação', {
                     'fields': ('obs', ),
                     'classes': ('collapse',)
                 }),
    )

    list_display = ('fornecedor', '__unicode__', 'isbn', 'editora')

    form = PublicacaoAdminForm

    list_per_page = 10

    search_fields = ('obs', 'isbn', 'titulo', 'autor', 'editora')

admin.site.register(Publicacao, PublicacaoAdmin)



class EquipamentoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'ano' e 'processo' do protocolo,
                         'nome' do estado,
                         'ns', 'marca', 'modelo', 'nome' e 'part_number' do modelo equipamento.
    """

    fieldsets = (

                 ('Protocolo', {
                     'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
                     'classes': ('wide',)
                 }),
                 ('Equipamento', {
                     'fields': ('equipamento_esta', 'nome', ('marca', 'modelo', 'ns'), 'part_number'),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('fornecedor', 'nome', 'marca', 'modelo', 'ns')

    form = EquipamentoAdminForm

    list_per_page = 10
    inlines = [HistoricoLocalInline]
    search_fields = ('ns', 'marca', 'modelo', 'nome', 'part_number', 'pagamento__conta_corrente__cod_oper')
    list_filter = (Termos,)

admin.site.register(Equipamento, EquipamentoAdmin)

class MovelAdmin(admin.ModelAdmin):

    fieldsets = (
                 ('Protocolo', {
		      'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
		      'classes': ('wide',)
		 }),
		 (u'Móvel', {
		      'fields': ('descricao', 'imagem'),
		      'classes': ('wide',)
		 }),
    )

    list_display = ('descricao', 'valor')
    form = MovelAdminForm
    list_filter = (Termos,)
    search_fields = ('pagamento__conta_corrente__cod_oper', 'descricao')

admin.site.register(Movel, MovelAdmin)


class MonitoramentoInternoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'ano' e 'processo' do protocolo,
                         'nome' do estado,
                         'ns', 'marca', 'modelo', 'nome', 'part_number' e 'community' do roteador.
    """

    fieldsets = (

                 ('Protocolo', {
                     'fields': (('termo', 'protocolo'), 'pagamento'),
                     'classes': ('wide',)
                 }),
                 ('Roteador', {
                     'fields': (('marca', 'modelo', 'ns'), 'nome', 'part_number', 'community'),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('fornecedor', 'nome', 'marca', 'modelo', 'ns', 'community')

    form = MonitoramentoInternoAdminForm

    list_per_page = 10

    search_fields = ('ns', 'marca', 'modelo', 'nome', 'part_number', 'community')

admin.site.register(MonitoramentoInterno, MonitoramentoInternoAdmin)



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

    search_fields = ['endereco__identificacao____entidade__nome', 'endereco__identificacao__entidade__sigla', 'endereco__identificacao__contato__nome', 'endereco__identificacao__funcao', 'endereco__identificacao__area', 'endereco__rua', 'endereco__complemento', 'endereco__bairro', 'endereco__cidade', 'endereco__estado', 'endereco__cep', 'endereco__pais', 'descrica', 'data']

admin.site.register(HistoricoLocal, HistoricoLocalAdmin)

