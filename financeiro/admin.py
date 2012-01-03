# -*- coding: utf-8 -*-
from models import *
from forms import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from memorando.models import Corpo

#class AuditoriaQuestionaInline(admin.TabularInline):
#    model = Corpo.pagamento.through

class PagamentoInline(admin.TabularInline):
    
    fieldsets = ((None, {'fields':('termo', 'valor_fapesp', 'protocolo', 'origem_fapesp', 'valor_patrocinio')}),)
    model = Pagamento
    extra = 1
    form = PagamentoAdminForm

class AuditoriaInline(admin.TabularInline):
    model = Auditoria
    choices = 1
  
class ExtratoCCAdmin(admin.ModelAdmin):
    
    fieldsets = (
		  (None, {
			  'fields': (('termo', 'extrato_financeiro', 'despesa_caixa'), ('data_oper', 'cod_oper'), ('historico', 'valor')),
			  'classes': ('wide',)
		  }),
		  ('Extras', {
			  'fields': ('data_extrato', 'imagem', 'capa', 'obs'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('data_oper', 'cod_oper', 'historico', 'valor')
    list_filter = ('data_oper',)
    search_fields = ('cod_oper',)
    inlines = (PagamentoInline,)
    form = ExtratoCCAdminForm
    
class ExtratoFinanceiroAdmin(admin.ModelAdmin):
    
    fieldsets = (
		  (None, {
			  'fields': (('termo', 'data_libera'), ('cod', 'valor'), ('comprovante', 'tipo_comprovante'), 'parcial'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('termo', 'data_libera', 'cod', 'historico', 'valor')
    list_filter = ('termo',)
    
    
class PagamentoAdmin(admin.ModelAdmin):
    
    fieldsets = (
		  (None, {
			  'fields': (('cod_oper', 'conta_corrente', 'patrocinio'), ('termo', 'numero', 'protocolo'), ('valor_fapesp', 'valor_patrocinio')),
			  'classes': ('wide',)
		  }),
		  ('Outros', {
			  'fields': (('reembolso', 'membro'),'origem_fapesp', 'pergunta'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('item', 'nota', 'data', 'codigo_operacao', 'formata_valor_fapesp', 'parcial', 'pagina')
    search_fields = ('protocolo__num_documento', 'conta_corrente__cod_oper', 'protocolo__descricao2__descricao', 'protocolo__descricao2__entidade__sigla', 'protocolo__referente')
    form = PagamentoAdminForm
    inlines = (AuditoriaInline, )
    list_filter = ('protocolo__termo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade', 'conta_corrente__extrato_financeiro')
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
    
    list_display = ('localiza', 'data_oper', 'historico', 'valor')
    
class AuditoriaAdmin(admin.ModelAdmin):
  
    fieldsets = (
		  (None, {
			  'fields': (('estado', 'pagamento', 'tipo'), ('parcial', 'pagina', 'arquivo'), 'obs'),
			  'classes': ('wide',)
		  }),
    )
    
    list_display = ('pagamento', 'tipo', 'parcial', 'pagina')

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
