from django.contrib import admin
from models import *

class EventoAdmin(admin.ModelAdmin):
    fieldsets = (
                 (None,
                  {'fields': ('acordo', ('tipo', 'local'), 'descricao', ('inicio', 'termino'), 'url', 'obs')}),
                )
  
    list_display = ('tipo', 'local', 'descricao', 'inicio')
    search_fields = ('descricao',)

admin.site.register(Tipo)
admin.site.register(Evento, EventoAdmin)
admin.site.register(AreaPrograma)

class AtribuicaoInline(admin.TabularInline):
    model = Atribuicao
    extra = 1

class SessaoAdmin(admin.ModelAdmin):
    fieldsets = (
                 (None, 
                  {'fields': ('area', ('evento', 'descricao'), ('local', 'inicio', 'termino'), 'arquivo', 'obs')}),
                )
    list_display = ('descricao', 'inicio', 'termino')
    inlines = [AtribuicaoInline,]
    search_fields = ('area__nome', 'descricao')

admin.site.register(Sessao, SessaoAdmin)
admin.site.register(AreaOperacional)
