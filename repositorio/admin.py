# -*- coding: utf-8 -*-
from django.contrib import admin
from repositorio.models import Repositorio, Ticket, Tipo, Estado, Natureza, Servico
from repositorio.forms import RepositorioAdminForm

class TicketInline(admin.TabularInline):
	model = Ticket
	extra = 1
	
class RepositorioAdmin(admin.ModelAdmin):
	"""
	Interface administrativa para o repositório
	"""
	inlines = [TicketInline]
	form = RepositorioAdminForm
	
	fieldsets = (
		(None, {
			'fields': ('data_ocorrencia', ('tipo', 'natureza', 'estado'), 'servicos', 'ocorrencia', 'memorandos', ('filtra_patrimonio', 'patrimonios'), ('responsavel', 'demais'), 'obs'),
			'classes': 'wide',
		}),
	)
	
	readonly_fields = ('num_rep',)
	list_display = ('num_rep', 'data', 'data_ocorrencia', 'tipo', 'natureza', 'estado')
	search_fields = ('ocorrencia', 'tipo__nome', 'natureza__nome')
	
# Register your models here.
admin.site.register(Repositorio, RepositorioAdmin)
admin.site.register(Tipo)
admin.site.register(Natureza)
admin.site.register(Estado)
admin.site.register(Servico)
