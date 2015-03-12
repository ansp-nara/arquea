# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class PapelariaAdmin(admin.ModelAdmin):
    
    fieldsets = ((u'Papel timbrado retrato A4', {
                        'fields': ('papel_timbrado_retrato_a4', ('retrato_a4_margem_superior', 'retrato_a4_margem_inferior')),
                        }),
                 (u'Papel timbrado paisagem A4', {
                        'fields': ('papel_timbrado_paisagem_a4', ('paisagem_a4_margem_superior', 'paisagem_a4_margem_inferior')),
                        }),
                 (u'Papel timbrado retrato A3', {
                        'fields': ('papel_timbrado_retrato_a3', ('retrato_a3_margem_superior', 'retrato_a3_margem_inferior')),
                        }),
                 (u'Papel timbrado paisagem A3', {
                        'fields': ('papel_timbrado_paisagem_a3', ('paisagem_a3_margem_superior', 'paisagem_a3_margem_inferior')),
                        }),
                 (None, {
                        'fields': ('valido',)
                        }),
                )
    list_per_page = 10
    list_display = ('valido', 'papel_timbrado_retrato_a4', 'papel_timbrado_paisagem_a4','papel_timbrado_retrato_a3', 'papel_timbrado_paisagem_a3')
    
admin.site.register(Papelaria, PapelariaAdmin)


class ChequeAdmin(admin.ModelAdmin):
    
    list_per_page = 10
    list_display = ('nome_assinatura',)
    
admin.site.register(Cheque, ChequeAdmin)


class VariavelAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('nome', 'valor')
    
admin.site.register(Variavel, VariavelAdmin)

