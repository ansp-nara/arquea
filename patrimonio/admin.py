# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from utils.functions import clone_objects
from models import *
from forms import *

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
                   'fields':(('entidade',), ('endereco', 'posicao'), ('descricao', 'data', 'estado', 'memorando'))
                }),)
    model = HistoricoLocal
    fk_name = 'patrimonio'
    formset = HistoricoLocalAdminFormSet
    form = HistoricoLocalAdminForm
    choices = 1
    extra = 1


class PatrimonioAdmin(admin.ModelAdmin):
    fieldsets = (
                 ('Pagamento', {
                      'fields': (('termo', 'npgto',), ('pagamento', 'valor',)),
                      'classes': ('wide',)
                 }),
                 ('Geral', {
                      'fields': (('checado', 'tipo', 'apelido', 'tem_numero_fmusp', 'numero_fmusp'), ('part_number', 'ns', 'ncm', 'ean', 'agilis'), 
                                 ('nf', 'patrimonio'), 'descricao', ('complemento', 'tamanho'), ('modelo',), 
                                 ('procedencia', 'entidade_procedencia',),('filtro_equipamento', 'equipamento',))
                 }),
                 ('Extras', {
                      'classes': ('collapse',),
                      'fields': ('imagem', 'especificacao', 'obs', 'titulo_autor', 'isbn',),
                 }),
                 ('Patrimônios contidos', {
                      'classes': ('collapse',),
                      'fields': ('form_filhos',),
                 }),

    )
    #readonly_fields = ('equipamento__entidade_fabricante',)
    form = PatrimonioAdminForm
    list_display = ('tipo', 'descricao', 'complemento', 'posicao', 'agilis', 'modelo', 'ns', 'nf', 'valor', 'checado')
    list_filter = ('tipo', 'pagamento__protocolo__termo',)
    inlines = [HistoricoLocalInline,]
    search_fields = ('descricao', 'ns', 'pagamento__protocolo__num_documento', 'ncm', 'historicolocal__descricao', 'equipamento__entidade_fabricante__sigla', 'part_number', 'modelo', 'historicolocal__posicao', 'apelido')
    actions = ['action_mark_agilis', 'action_unmark_agilis', 'action_mark_checado', 'action_clone']


    def __init__(self, model, admin_site):
        """
        Utilizado para setar o admin_site para o forms
        """
        self.form.admin_site = admin_site
        super(PatrimonioAdmin, self).__init__(model, admin_site)
        
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

    search_fields = ['endereco__endereco__entidade__nome', 'endereco__endereco__entidade__sigla', \
                     'endereco__endereco__rua', 'endereco__endereco__compl', 'endereco__endereco__bairro', \
                     'endereco__endereco__cidade', 'endereco__endereco__estado', 'endereco__endereco__cep', \
                     'endereco__endereco__pais', 'descricao', 'data', \
                     'patrimonio__pagamento__protocolo__descricao', 'patrimonio__pagamento__protocolo__protocolo__num_documento', 'patrimonio__pagamento__protocolo__protocolo__descricao']

admin.site.register(HistoricoLocal, HistoricoLocalAdmin)

class EquipamentoAdmin(admin.ModelAdmin):
    search_fields = ['part_number', 'descricao']
    list_display = ('descricao', 'part_number', 'tipo')
    
    form = EquipamentoAdminForm
    
    def __init__(self, model, admin_site):
        """
        Utilizado para setar o admin_site para o forms
        """
        self.form.admin_site = admin_site
        super(EquipamentoAdmin, self).__init__(model, admin_site)

admin.site.register(Equipamento, EquipamentoAdmin)



