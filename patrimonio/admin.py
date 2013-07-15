# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.utils.translation import ugettext_lazy as _
from forms import *
from django.utils.encoding import smart_unicode
from utils.functions import clone_objects


admin.site.register(Estado)
admin.site.register(Tipo)
admin.site.register(Dimensao)
admin.site.register(Distribuicao)
admin.site.register(DistribuicaoUnidade)
admin.site.register(UnidadeDimensao)
admin.site.register(Direcao)
admin.site.register(TipoEquipamento)

class HistoricoLocalInline(admin.StackedInline):
    fieldsets = (('', {
                   'fields':(('entidade'), ('endereco', 'posicao'), ('descricao', 'data', 'estado', 'memorando'))
                }),)
    model = HistoricoLocal
    form = HistoricoLocalAdminForm
    fk_name = 'patrimonio'
    choices = 1
    extra = 1

class PatrimonioAdmin(admin.ModelAdmin):
    """ 
    fieldsets = (
                 ('Pagamento', {
		      'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
                      'classes': ('wide',)
                 }),
	         ('Geral', {
		      'fields': (('checado', 'apelido', 'tipo', 'numero_fmusp'), ('equipamento', 'ean', 'agilis'), ('nf', 'patrimonio'), ('complemento', 'procedencia'))
                 }),
 	         ('Extras', {
		      'fields': ('obs',),
		      'classes': ('collapse',)
                 }),
    )
    """
    fieldsets = (
                 ('Pagamento', {
                      'fields': (('termo', 'npgto'), ('pagamento', 'valor')),
                      'classes': ('wide',)
                 }),
                 ('Geral', {
                      'fields': (('checado', 'tipo', 'apelido', 'tem_numero_fmusp', 'numero_fmusp'), ('part_number', 'ns', 'ncm', 'ean', 'agilis'), ('nf', 'patrimonio'), 'descricao', ('complemento', 'tamanho'), ('marca', 'modelo', 'procedencia'), 'equipamento')
                 }),
                 ('Extras', {
                      'fields': ('imagem', 'especificacao', 'obs', 'titulo_autor', 'isbn'),
                      'classes': ('collapse',)
                 }),
    )

    form = PatrimonioAdminForm
    list_display = ('tipo', 'descricao', 'complemento', 'posicao', 'agilis', 'marca', 'modelo', 'ns', 'nf', 'valor', 'checado')
    list_filter = ('tipo', 'pagamento__protocolo__termo',)
    inlines = [HistoricoLocalInline,]
    search_fields = ('descricao', 'ns', 'pagamento__protocolo__num_documento', 'ncm', 'historicolocal__descricao', 'marca', 'part_number', 'modelo', 'historicolocal__posicao', 'apelido')
    actions = ['action_mark_agilis', 'action_unmark_agilis', 'action_mark_checado', 'action_clone']

    def action_clone(self, request, queryset):
        objs = clone_objects(queryset)
        total = queryset.count()
        if total == 1:
            message = u'1 patrimônio copiado'
        else:
            message = u'%s patrimônios copiados' % total
        self.message_user(request, message)

    action_clone.short_description = _(u"Duplicar os patrimônios selecionados")

    def action_mark_agilis(self, request, queryset):
	queryset.update(agilis=True)
    action_mark_agilis.short_description = _(u'Marcar para o Agilis')

    def action_unmark_agilis(self, request, queryset):
        queryset.update(agilis=False)
    action_unmark_agilis.short_description = _(u'Desmarcar para o Agilis')

    def action_mark_checado(self, request, queryset):
        queryset.update(checado=True)
    action_mark_checado.short_description = _(u'Marcar como checado')

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

class EquipamentoAdmin(admin.ModelAdmin):
    search_fields = ['part_number', 'descricao']
    list_display = ('descricao', 'part_number', 'tipo')

admin.site.register(Equipamento, EquipamentoAdmin)
