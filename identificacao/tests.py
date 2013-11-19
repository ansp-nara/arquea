# -*- coding: utf-8 -*-

from django.test import TestCase
from identificacao.models import *

class IdentificacaoTest(TestCase):
    def setUp(self):
        ent, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'Global Crossing', 'cnpj': '00.000.000/0000-00', 'fisco': True, 'url': ''})
        c, created = Contato.objects.get_or_create(primeiro_nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': '', 'ativo': True})
        endereco, created = Endereco.objects.get_or_create(entidade=ent)
        iden, created = Identificacao.objects.get_or_create(endereco=endereco, contato=c, defaults={'funcao':'Tecnico', 'area':'', 'ativo': True})

    def test_unicode(self):
        iden = Identificacao.objects.get(pk=1)
        self.assertEquals(iden.__unicode__(), u'SAC - Joao')
        
    def test_unicode_com_area(self):
        iden = Identificacao.objects.get(pk=1)
        iden.area = 'TI'
        self.assertEquals(iden.__unicode__(), u'SAC - TI - Joao')