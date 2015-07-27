# -*- coding: utf-8 -*-
import django
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from financeiro.models import *
from financeiro.forms import *
from utils.admin import PrintModelAdmin
from utils.admin import RelatedOnlyFieldListFilter
from rede.models import Recurso
from utils.button import ButtonAdmin, Button
from django.http import HttpResponseRedirect

class RecursoInline(admin.StackedInline):
    model = Recurso
    extra = 2
    form = RecursoInlineAdminForm
    fieldsets = ((None, {'fields':('planejamento',('quantidade','mes_referencia','ano_referencia'), ('valor_mensal_sem_imposto','valor_imposto_mensal'),'obs')}),)

    def __init__(self, model, admin_site):
        """
        Utilizado para setar o admin_site para o forms
        """
        self.form.admin_site = admin_site
        super(RecursoInline, self).__init__(model, admin_site)


#class AuditoriaQuestionaInline(admin.TabularInline):
#    model = Corpo.pagamento.through

class PagamentoInline(admin.TabularInline):
    
    fieldsets = ((None, {'fields':('termo', 'valor_fapesp', 'protocolo', 'origem_fapesp', 'valor_patrocinio')}),)
    model = Pagamento
    extra = 1
    form = PagamentoAdminForm

class AuditoriaInline(admin.TabularInline):
    form = PagamentoAuditoriaAdminInlineForm
    model = Auditoria
    choices = 1

  
class ExtratoCCAdmin(admin.ModelAdmin):
    
    fieldsets = (
		  (None, {
			  'fields': (('termo', 'extrato_financeiro', 'despesa_caixa', 'cartao'), ('data_oper', 'cod_oper'), ('historico', 'valor')),
			  'classes': ('wide',)
		  }),
		  ('Extras', {
			  'fields': ('data_extrato', 'imagem', 'capa', 'obs'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('data_oper', 'cod_oper', 'historico', 'valor')
    search_fields = ('cod_oper',)
    inlines = (PagamentoInline,)
    form = ExtratoCCAdminForm
    
class ExtratoFinanceiroAdmin(ButtonAdmin):
    
    fieldsets = (
		  (None, {
			  'fields': (('termo', 'data_libera'), ('cod', 'valor'), ('comprovante', 'tipo_comprovante'), 'parcial', 'taxas'),
			  'classes': ('wide',)
		  }),
    )

    buttons = (
        Button('save_and_insert_cc', 'Salvar e inserir entrada no extrato de conta corrente', needSuperUser=False),
    )

    def tool_save_and_insert_cc(self, request, obj, button):
        """
        Tratamento do novo botão de "Salvar e inserir extrato c/c"
        """
        retorno = ExtratoFinanceiro._insere_extrato_cc(obj)
         
        if (retorno == 1):
            messages.add_message(request, messages.SUCCESS, u"Extrato de conta corrente inserido com sucesso.")
        elif (retorno == 2):
            messages.add_message(request, messages.WARNING, u"Extrato de conta corrente já existente.")
        else:
            messages.add_message(request, messages.WARNING, u"Extrato de conta corrente não inserido.")

        return HttpResponseRedirect(reverse('admin:financeiro_extratofinanceiro_changelist'))


    list_display = ('termo', 'data_libera', 'cod', 'historico', 'valor')
    list_filter = ('termo',)
    search_fields = ('historico',)
    form = ExtratoFinanceiroAdminForm



class PagamentoAdmin(PrintModelAdmin):
    
    fieldsets = (
		  (None, {
			  'fields': (('cod_oper', 'conta_corrente', 'patrocinio'), 
                         ('termo', 'numero', 'protocolo'), 
                         ('valor_fapesp', 'valor_patrocinio')),
			  'classes': ('wide',)
		  }),
		  ('Outros', {
			  'fields': (('reembolso', 'membro'),'origem_fapesp', 'pergunta'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('item', 'nota', 'data', 'codigo_operacao', 'formata_valor_fapesp', 'parcial', 'pagina')
    # list_select_related pode ser somente boolean no 1.5
    if django.VERSION[0:2] >= (1, 6):
        list_select_related = ('protocolo', 'origem_fapesp', 'origem_fapesp__item_outorga', 'origem_fapesp__item_outorga__natureza_gasto__modalidade', 'origem_fapesp__item_outorga__natureza_gasto__termo',)
    else:
        list_select_related = True
    
    search_fields = ('protocolo__num_documento', 'conta_corrente__cod_oper', 'protocolo__descricao2__descricao', 'protocolo__descricao2__entidade__sigla', 'protocolo__referente')
    form = PagamentoAdminForm
    inlines = (AuditoriaInline, RecursoInline)
    list_filter = ('protocolo__termo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade')
    filter_horizontal = ('pergunta',)
   
    def lookup_allowed(self, key, value):
        if key in ('origem_fapesp__item_outorga'):
            return True
        return super(PagamentoAdmin, self).lookup_allowed(key, value)
 
class ExtratoPatrocinioAdmin(admin.ModelAdmin):
  
    fieldsets = (
		  (None, {
			  'fields': ('localiza', ('data_oper', 'cod_oper', 'historico', 'valor'), 'obs'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('localiza', 'cod_oper', 'data_oper', 'historico', 'valor')
    search_fields = ('cod_oper',)
    ordering = ('-data_oper',)
    form = ExtratoPatrocinioAdminForm
    

class AuditoriaAdmin(admin.ModelAdmin):
  
    fieldsets = (
		  (None, {
			  'fields': (('estado', 'pagamento', 'tipo'), ('parcial', 'pagina', 'arquivo'), 'obs'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('pagamento', 'tipo', 'parcial', 'pagina')
    # list_select_related pode ser somente boolean no 1.5
    if django.VERSION[0:2] >= (1, 6):
        list_select_related = ('tipo', 'pagamento__protocolo', 'pagamento__origem_fapesp', \
                       'pagamento__origem_fapesp__item_outorga', \
                       'pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade', \
                       'pagamento__origem_fapesp__item_outorga__natureza_gasto__termo',)
    else:
        list_select_related = True

    search_fields = ('parcial', 'pagina')
    list_filter = (('tipo', RelatedOnlyFieldListFilter), 
                   ('estado', RelatedOnlyFieldListFilter),
                   )
    form = AuditoriaAdminForm

    def get_queryset(self, request):
        queryset = super(AuditoriaAdmin, self).get_queryset(request)
        return queryset
        
    def __init__(self, model, admin_site):
        """
        Utilizado para setar o admin_site para o forms
        """
        self.form.admin_site = admin_site
        super(AuditoriaAdmin, self).__init__(model, admin_site)
    

class EstadoAdmin(admin.ModelAdmin):
    search_fields = ('nome',)

class LocalizaPatrocinioAdmin(admin.ModelAdmin):
    search_fields = ('consignado',)

class TipoComprovanteAdmin(admin.ModelAdmin):
    search_fields = ('nome',)

class TipoComprovanteFinanceiroAdmin(admin.ModelAdmin):
    search_fields = ('nome',)

admin.site.register(Estado, EstadoAdmin)
admin.site.register(TipoComprovante, TipoComprovanteAdmin)
admin.site.register(LocalizaPatrocinio, LocalizaPatrocinioAdmin)
admin.site.register(ExtratoCC, ExtratoCCAdmin)
admin.site.register(ExtratoFinanceiro, ExtratoFinanceiroAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(ExtratoPatrocinio, ExtratoPatrocinioAdmin)
admin.site.register(Auditoria, AuditoriaAdmin)
admin.site.register(TipoComprovanteFinanceiro, TipoComprovanteFinanceiroAdmin)

