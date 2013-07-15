# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from forms import *
from django.contrib.admin import SimpleListFilter
from identificacao.models import Entidade

class DesignadoFilter(SimpleListFilter):
    title = u'designado'
    parameter_name = 'designado'

    def lookups(self, request, model_admin):
        entidade_ids = BlocoIP.objects.values_list('designado', flat=True).distinct()
        return [(e.id, e.sigla) for e in Entidade.objects.filter(id__in=entidade_ids)]

    def queryset(self, request, queryset):
        id=self.value()
        if id:
            return queryset.filter(designado__id__exact=id)
        else: return queryset

class UsuarioFilter(SimpleListFilter):
    title = u'usado por'
    parameter_name = 'usado'

    def lookups(self, request, model_admin):
        entidade_ids = BlocoIP.objects.values_list('usuario', flat=True).distinct()
        return [(e.id, e.sigla) for e in Entidade.objects.filter(id__in=entidade_ids)]

    def queryset(self, request, queryset):
        id=self.value()
        if id:
            return queryset.filter(usuario__id__exact=id)
        else: return queryset

class SuperblocoFilter(SimpleListFilter):
    title = 'tipo de bloco'
    parameter_name = 'bloco'

    def lookups(self, request, model_admin):
        return [('super', 'Apenas super blocos')]

    def queryset(self, request, queryset):
        if self.value() == 'super':
	    return queryset.filter(superbloco__isnull=True)
        return queryset

class BlocoIPAdmin(admin.ModelAdmin):

    fieldsets = (
		 (None, {
			 'fields': (('ip', 'mask'), ('asn', 'proprietario'), ('designado', 'usuario'), ('superbloco', 'rir'), 'obs'),
			 'classes': ('wide',)
			}
		),
		)
    list_display = ('cidr', 'asn', 'proprietario', 'usu', 'desig', 'rir', 'obs')
    search_fields = ('asn__entidade__sigla', 'ip')
    list_filter = (SuperblocoFilter, 'asn', 'proprietario', DesignadoFilter, UsuarioFilter)

admin.site.register(BlocoIP, BlocoIPAdmin)

class SegmentoInline(admin.StackedInline):
    fieldsets = (
		 (None, {
			 'fields': (('operadora', 'banda', 'link_redundante'), ('data_ativacao', 'data_desativacao', 'uso', 'sistema', 'canal'), ('designacao', 'interfaces'), 'obs'),
			 'classes': ('wide',)
			}
		 ),
		)

    model = Segmento
    extra = 1

class EnlaceAdmin(admin.ModelAdmin):
    search_fields = ('participante__entidade__sigla',)

    inlines = [SegmentoInline]
    #list_display = ('participante_display', 'entrada_display', 'banda', 'operadora')

admin.site.register(Operadora)
admin.site.register(EnlaceOperadora)
admin.site.register(Banda)
admin.site.register(IPBorda)
admin.site.register(Enlace, EnlaceAdmin)

class RecursoAdmin(admin.ModelAdmin):
    form = RecursoAdminForm

    fieldsets = (
                 (None, {
                         'fields': ('planejamento', ('termo', 'pagamento'), 'obs', ('quantidade', 'valor_imposto_mensal', 'valor_mensal_sem_imposto'), ),
                         'classes': ('wide',)
                        }
                 ),
                )

class BeneficiadoInline(admin.TabularInline):
    model = Beneficiado
    extra = 2

class PlanejaAquisicaoRecursoAdmin(admin.ModelAdmin):

    form = PlanejaAquisicaoRecursoAdminForm
    fieldsets = (
                 (None, {
                         'fields': (('os', 'ano'), ('tipo', 'referente'), ('quantidade', 'valor_unitario'), ('projeto', 'unidade', 'instalacao'), 'banda', 'obs'),
                         'classes': ('wide',)
                        }
                 ),
                )
    list_display = ('projeto', 'quantidade', 'tipo', 'os', 'referente', 'valor_unitario', 'instalacao')

    search_fields = ('os__numero', 'referente', 'tipo__nome')

    inlines = [BeneficiadoInline]

admin.site.register(TipoServico)
admin.site.register(Projeto)
admin.site.register(Unidade)
admin.site.register(Recurso, RecursoAdmin)
admin.site.register(PlanejaAquisicaoRecurso, PlanejaAquisicaoRecursoAdmin)
admin.site.register(RIR)

admin.site.register(Segmento)
admin.site.register(Canal)
admin.site.register(Interface)
admin.site.register(Uso)
admin.site.register(Sistema)
admin.site.register(Estado)
