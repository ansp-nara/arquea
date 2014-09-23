# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from patrimonio.models import Patrimonio

class Command(BaseCommand):
    help = u'Envia as informações de prestação de contas para o sistema Agilis'
    
    def handle(self, *args, **options):
        
        for p in Patrimonio.objects.filter(apelido__isnull=False):
            print "%s;%s" % (p.apelido, p.id)
