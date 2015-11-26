from django.contrib import admin
from abuse.models import Tipo, Instituicao, Mensagem


class MensagemAdmin(admin.ModelAdmin):
    list_filter = ('instituicao', 'tipo', 'data')

admin.site.register(Tipo)
admin.site.register(Instituicao)
admin.site.register(Mensagem, MensagemAdmin)
