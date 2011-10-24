#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

import sys
from datetime import date

from financeiro.models import ExtratoCC

if len(sys.argv) < 2:
    sys.exit("Nome de arquivo faltando")
    
entradas = []
total = 0.0

arq = open(sys.argv[1])

for l in arq:
    if l.find('DATA EMISS') > -1:
        d = l.split()[2]
        (dia, mes, ano) = d.split('/')
        emissao = date(int(ano), int(mes), int(dia))

    elif len(l) > 60:
        if l.find('LIBERACAO DEPOSITO CHEQ') > -1: continue
        campos = l.rstrip().split()
        if len(campos) < 4: continue
        data = campos[0].split('/')
        if len(data) < 2: continue
        valor = campos.pop()
        numero = int(campos.pop())
        descricao = ' '.join(campos[1:])
        dc = valor[-1]
        valor = valor.rstrip(dc)
        v1 = valor.split(',')
        v2 = v1[0].split('.')
        int_part = ''.join(v2)
        dec_part = v1[1]
        valor = int_part+'.'+dec_part
        valor = float(valor)
        dt = date(int(ano), int(data[1]), int(data[0]))
        if dt > emissao:
            dt = date(int(ano)-1, int(data[1]), int(data[0]))
        if dc == 'D': valor = -valor
	n = ExtratoCC.objects.filter(data_oper=dt, cod_oper=numero, valor=str(valor), historico=descricao).exclude(data_extrato=emissao).count()
	if not n:
	    ex = ExtratoCC.objects.create(data_oper=dt, cod_oper=numero, valor=str(valor), historico=descricao, data_extrato=emissao)
