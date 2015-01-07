# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from patrimonio.models import Patrimonio
from optparse import make_option
import sys

class Command(BaseCommand):
    help = u'Envia as informações de prestação de contas para o sistema Agilis'
    option_list = BaseCommand.option_list + (
        make_option('--apelido',
            action='store_true',
            dest='apenas_apelido',
            default=False,
            help='Lista apenas equipamentos que tenham apelido'),
        make_option('--saida',
            dest='filename',
            default=None,
            help='Arquivo onde será gravada a saída'),
        make_option('--filtro',
            dest='filtro',
            default=None,
            help='Filtro de localização'),     
        )
            
        
    def handle(self, *args, **options):
        
        patrimonios = Patrimonio.objects.filter(patrimonio__apelido__contains='Rack')

        if options['apenas_apelido']:
            patrimonios = patrimonios.filter(apelido__isnull=False).exclude(apelido='')
                
        if options['filename']:
            f = open(options['filename'], 'w')
        else:
            f = sys.stdout
            
        if patrimonios.count() > 0:
            f.write('apelido;codigo\n')
        for p in patrimonios:
            if options['filtro']:
                
                if p.historico_atual:
                    if p.historico_atual.__unicode__().find(options['filtro']) >= 0:
                        f.write('%s;%s\n' % (p.apelido, p.id))
            else:
                f.write('%s;%s\n' % (p.apelido, p.id))
