# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.utils.translation import ugettext_lazy as _
from forms import *

class PerguntaInline(admin.TabularInline):
    fieldsets = ((None, {'fields': ('numero', 'questao')}),)
    model = Pergunta
    form = PerguntaAdminForm
    extra = 2


class MemorandoFAPESPAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('termo', 'numero'), 'arquivo')}),)
    inlines = [PerguntaInline]
    list_per_page = 10
    list_display = ('termo', 'numero')


class CorpoInline(admin.TabularInline):
    fieldsets = ((None, {'fields': ('pergunta', 'perg', 'resposta', 'anexo')}),)
    form = CorpoAdminForm
    formset = CorpoFormSet
    model = Corpo
    extra = 2

class MemorandoRespostaAdmin(admin.ModelAdmin):
    fieldsets = (

                (_(u'Memorando'), {
                    'fields': (('memorando', 'assunto'), 'identificacao', 'estado'), 
                 }),
                (None, {
                    'fields': ('introducao', 'conclusao', ('assinatura', 'data'), 'arquivo', 'protocolo'),
                 }),

                (_(u'Observação'), {
                    'fields': ('obs', ),
                    'classes': ('collapse',)
                 }),
    )
    inlines = [CorpoInline]
    list_display = ('__unicode__', 'termo', 'memorando', 'assunto')
    form = MemorandoRespostaForm

admin.site.register(Estado)
admin.site.register(MemorandoFAPESP, MemorandoFAPESPAdmin)
admin.site.register(MemorandoResposta, MemorandoRespostaAdmin)
admin.site.register(Assunto)

class MemorandoSimplesAdmin(admin.ModelAdmin):
    form = MemorandoSimplesForm
    list_display = ('__unicode__', 'assunto', 'data')

admin.site.register(MemorandoSimples, MemorandoSimplesAdmin)

