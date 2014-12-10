from django.core.management.base import BaseCommand, CommandError
import sys
from datetime import date
import re
from decimal import Decimal
from financeiro.models import ExtratoCC


class Command(BaseCommand):
    args = u'<arquivo_extrato cc/ct >'
    help = 'Carrega um extrato de conta corrente'
    
    def handle(self, *args, **options):
        if len(args) < 2:
            self.stdout.write('Nome de arquivo faltando')
            return
        
        arq = open(args[0])
        for l in arq:
            dados = l.split()
            if args[1] == 'cc':
                data = dados.pop(0)
                sinal = dados.pop()
                valor = dados.pop()
                codigo = dados.pop()
                historico = ' '.join(dados)
                cartao = False
            else:
                codigo = dados[0]
                data = dados[1]
                valor = dados[2]
                sinal = dados[3]
                historico = ' '.join(dados[5:-3])
                cartao = True

            (d, m, y) = map(int, data.split('/'))
            if y < 2000: y += 2000
            data = date(y,m,d)
            valor = re.sub('\.', '', valor)
            valor = re.sub(',', '.', valor)
            codigo = re.sub('\.', '', codigo)
            sinal = '' if sinal=='C' else '-'
            ex = ExtratoCC.objects.create(data_oper=data, cod_oper=codigo, valor=Decimal('%s%s' % (sinal, valor)), historico=historico, despesa_caixa=False, cartao=cartao)
            
        self.stdout.write('Extrato inserido')
