import sys
from decimal import Decimal
import datetime

from django.core.management import setup_environ
import settings
setup_environ(settings)
sys.path.append('/var/lib/admin')
from financeiro.models import ExtratoFinanceiro

if len(sys.argv) < 2:
    print "Falta nome do arquivo"
    sys.exit()

arq = open(sys.argv[1])

for l in arq:
    try:
	int(l[0])
	dados = l.split()
	data = dados.pop(0)
	codigo = dados.pop(0)
	del dados[-1]
	del dados[-1]
	valor = dados.pop()
	historico = ' '.join(dados)

	sinal = valor[-1]
	valor = valor[:-1]
	valor = valor.replace('.','')
	valor = valor.replace(',','.')
	
	valor = sinal+valor
      
	d,m,a = data.split('/')

	print ano, proc, dv, historico, Decimal(valor), codigo, datetime.date(int('20'+a), int(m), int(d))
	ef = ExtratoFinanceiro(ano=int(ano), processo=int(proc), dv=int(dv), historico=historico, valor=Decimal(valor), cod=codigo, data_libera=datetime.date(int('20'+a), int(m), int(d)))
	ef.save()
    except ValueError:
	if l.find('Process') > -1:
	    processo = l.split()[1]
	    ano, resto = processo.split('/')
	    proc, dv = resto.split('-')
