# -*- coding: utf-8 -*-
from django.contrib import admin
from repositorio.models import Repositorio, Ticket, Tipo, Estado, Natureza, Servico, Anexo
from repositorio.forms import RepositorioAdminForm
from utils.admin import RelatedOnlyFieldListFilter


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


class AnexoInline(admin.TabularInline):
    model = Anexo
    extra = 1


class RepositorioAdmin(admin.ModelAdmin):
    """
    Interface administrativa para o repositório
    """
    inlines = [TicketInline, AnexoInline]
    form = RepositorioAdminForm

    fieldsets = (
        (None, {
            'fields': ('data_ocorrencia', ('tipo', 'natureza', 'estado'), 'servicos', 'ocorrencia', 'anterior',
                       'memorandos', ('filtra_patrimonio', 'patrimonios'), ('responsavel', 'demais'), 'obs'),
            'classes': 'wide',
        }),
    )

    readonly_fields = ('num_rep',)
    list_display = ('num_rep', 'data', 'data_ocorrencia', 'tipo', 'servicos_display', 'natureza', 'estado')
    search_fields = ('ocorrencia', 'tipo__nome', 'natureza__nome', 'servicos__nome')
    list_filter = (('tipo', RelatedOnlyFieldListFilter),  ('natureza', RelatedOnlyFieldListFilter),
                   ('estado', RelatedOnlyFieldListFilter),
                   )
#     def ocorrencia_trunc(self, obj):
#         ocorrencia_truncada = (obj.ocorrencia[:40] + '...') if len(obj.ocorrencia) > 40 else obj.ocorrencia
#         retorno = format_html('<div style="min-width: 145px;">%s</div>' % ocorrencia_truncada)
#         return retorno
#
#     ocorrencia_trunc.allow_tags = True
#     ocorrencia_trunc.short_description = 'ocorrencia'


# Register your models here.
admin.site.register(Repositorio, RepositorioAdmin)
admin.site.register(Tipo)
admin.site.register(Natureza)
admin.site.register(Estado)
admin.site.register(Servico)
