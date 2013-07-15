#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)
from patrimonio.models import *
from financeiro.models import Pagamento
from identificacao.models import EnderecoDetalhe
import csv
import datetime

tipo = Tipo.objects.get(nome='Definir NF')

planilha = csv.reader(open('/tmp/unicamp.csv', 'rb'), delimiter=';', quotechar='"')

for item in planilha:
    descricao = item[19].decode('iso-8859-1').encode('utf-8')
    modelo = item[0].decode('iso-8859-1').encode('utf-8')
    pn = item[1]
    ean = item[4]
    sn = item[5]
    ncm = item[10]
    nf = item[8]
    marca = item[7].decode('iso-8859-1').encode('utf-8')
    #local = item[23].split('-')
    #local.append(item[24])
    tamanho = None #item[25]
    ocorrencia = 'Inventariado' #item[17].decode('iso-8859-1').encode('utf-8')
    data = item[27]
    estado = item[22].decode('iso-8859-1').encode('utf-8')
    obs = item[28].decode('iso-8859-1').encode('utf-8')
    rev = item[2]
    ver = item[3]
    st = item[6]

    if rev: obs += 'Revision: %s' % rev
    if ver: obs += 'Version: %s' % ver
    if st: obs += 'Service Tag: %s' % st
    """
    while 1:
        try: local.remove('')
        except:break
    """
    e = EnderecoDetalhe.objects.get(id=11)
    """
    for p in local:
        try:
            e = e.enderecodetalhe_set.get(complemento=p)
        except:
            novo = EnderecoDetalhe()
            novo.detalhe = e
            novo.complemento = p
            novo.tipo_id = 3
            #novo.save()
            e = novo
    """
    patr = Patrimonio()
    if nf:
        pag = Pagamento.objects.filter(protocolo__num_documento__contains=int(nf), protocolo__termo__ano=2009)


        if pag.count() > 0:
            patr.pagamento = pag[0]
    #	print u'Pagamento da nota %s não cadastrado. Patrimônio não inserido' % nf
    #    continue

    #patr.pagamento = pag[0]
    patr.tipo = tipo
    patr.ns = sn
    patr.ean = ean
    patr.obs = obs
    patr.ncm = ncm
    patr.marca = marca
    patr.modelo = modelo
    patr.part_number = pn
    patr.descricao = descricao
    if tamanho: 
        tm = tamanho.split(',')
        if len(tm) == 1: patr.tamanho = tamanho
        else: patr.tamanho = '%s.%s' % tuple(tm)
    patr.save()
    print patr

    #if local == '': continue

    hc = HistoricoLocal()
    hc.endereco = e
    hc.descricao = ocorrencia
    (d,m,y) = map(int, data.split('/'))
    hc.data = datetime.date(y,m,d)
    status = Estado.objects.get(nome=estado)
    hc.estado = status
    hc.patrimonio = patr

    hc.save()
    print hc
