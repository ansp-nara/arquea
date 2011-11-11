from django.contrib import admin
from models import *

class BlocoIPAdmin(admin.ModelAdmin):

    list_display = ('asn', '__unicode__', 'obs')
    search_fields = ('asn__entidade__sigla', 'asn__entidade__nome', 'ip')

admin.site.register(BlocoIP, BlocoIPAdmin)
admin.site.register(Rota)
admin.site.register(Historico)
admin.site.register(Provedor)
