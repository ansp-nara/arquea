#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from django.core.mail import send_mail
from django.core.management import setup_environ
import settings
setup_environ(settings)

conn = psycopg2.connect("dbname=ANSP user=root password=abc123 host=10.0.1.137 port=5432")
cur = conn.cursor()

cur.execute("select uniclassifica.id as ID, unientidade.sigla as SIGLA, unientidade.url as URL from unientidade, uniendereco, uniclassifica, unitipo where unitipo.id = 33 and uniclassifica.papel_ = unitipo.id and uniclassifica.area_  = (select id from unitipo where tipo = 'pop' and nome = 'ANSP') and uniclassifica.subordinado_a  != (select id from unientidade where sigla = 'SES') and unientidade.id = uniendereco.id_unientidade and uniendereco.id = uniclassifica.id_uniendereco and uniclassifica.status_ = (select id from unitipo where tipo = 'status' and nome = 'ativo') order by sigla")

dados = cur.fetchall()

for dado in dados:
    cur.execute("select unientidade.nome as NOME, uniendereco.logradouro as LOGRADOURO, uniendereco.complemento as COMPLEMENTO, uniendereco.bairro as BAIRRO, uniendereco.cep as CEP, uniendereco.cidade as CIDADE, uniendereco.estado as ESTADO, uniendereco.pais as PAIS from unientidade, uniendereco where unientidade.id = uniendereco.id_unientidade and uniendereco.id = uniclassifica.id_uniendereco and uniclassifica.id = %s" % dado[0])
    inst = cur.fetchall()
    if len(inst) == 0: continue
    inst = inst[0]
    cur.execute("select distinct unicontato.nome as NOME, unicontato.email as EMAIL, unicontato.telefone as TELEFONE, unicontato.celular as CELULAR, unicontato.fax as FAX, (select nome from unitipo where unitipo.id = unicontato.funcao_) as FUNCAO_, (select nome from unitipo where unitipo.id = unicontato.cargo_) as CARGO_, unirel_contato.id_uniclassifica, unirel_contato.id_unicontato from unicontato, uniclassifica, unirel_contato, unitipo where unirel_contato.id_uniclassifica = %s AND unirel_contato.id_unicontato = unicontato.id AND unicontato.status_ = (select id from unitipo where tipo = 'status' and nome = 'ativo') order by nome" % dado[0])
    contatos = cur.fetchall()
    txt_cont = ''
    mails = []
    for c in contatos:
	txt_cont +='Nome: %s, email: %s, telefone(s): %s %s %s, tipo de contato: %s, cargo: %s\n' % c[:7]
	mails.append(c[1])

    msg = 'Instituição: %s, endereço: %s\n%s' % (inst[0], ' - '.join(inst[1:]), txt_cont)
    for c in contatos:
	send_mail('Contatos da Rede ANSP', msg, 'nara@ansp.br', ['antonio@ansp.br', 'ajoaoff@yahoo.com.br'])
