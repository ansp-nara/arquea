from django.contrib import admin
from models import *

class BlocoIPAdmin(admin.ModelAdmin):

    list_display = ('entidade', 'AS', '__unicode__', 'obs')
    search_fields = ('entidade__sigla', 'entidade__nome', 'ip')

admin.site.register(BlocoIP, BlocoIPAdmin)
