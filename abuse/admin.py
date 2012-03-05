from models import *
from django.contrib import admin

class MensagemAdmin(admin.ModelAdmin):
    list_filter = ('instituicao', 'tipo', 'data')

admin.site.register(Tipo)
admin.site.register(Instituicao)
admin.site.register(Mensagem, MensagemAdmin)
