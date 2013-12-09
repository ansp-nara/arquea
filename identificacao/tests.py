# -*- coding: utf-8 -*-

from django.test import TestCase
from identificacao.models import *

class IdentificacaoTest(TestCase):
    def setUp(self):
        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        c = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='', ativo=True)
        endereco = Endereco.objects.create(entidade=ent)
        iden = Identificacao.objects.create(endereco=endereco, contato=c, funcao='Tecnico', area='', ativo=True)

    def test_unicode(self):
        iden = Identificacao.objects.get(pk=1)
        self.assertEquals(iden.__unicode__(), u'SAC - Joao')
        
    def test_unicode_com_area(self):
        iden = Identificacao.objects.get(pk=1)
        iden.area = 'TI'
        self.assertEquals(iden.__unicode__(), u'SAC - TI - Joao')
        
        
class ContatoTest(TestCase):
    
    def setUp(self):
        ent1 = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        ent2 = Entidade.objects.create(sigla='GTECH', nome='Graneiro Tech', cnpj='00.000.000/0000-00', fisco=True, url='')
        c = Contato.objects.create(primeiro_nome='Joao', ultimo_nome=u"José da Silva Xavier", email='joao@joao.com.br', tel='', ativo=True)
        
        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)
        iden1 = Identificacao.objects.create(endereco=end1, contato=c, funcao='Tecnico', area='', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=c, funcao='Gerente', area='', ativo=True)


    def test_unicode(self):
        c = Contato.objects.get(pk=1)
        self.assertEquals(c.__unicode__(), u'Joao José da Silva Xavier')

    def test_nome_sem_sobrenome(self):
        c = Contato.objects.get(pk=1)
        c.ultimo_nome = None
        self.assertEquals(c.nome, u'Joao')

    def test_sem_nome(self):
        c = Contato.objects.get(pk=1)
        c.primeiro_nome = None
        c.ultimo_nome = None
        self.assertEquals(c.nome, None)

    def test_contato_entidade(self):
        c = Contato.objects.get(pk=1)
        c.area = 'TI'
        self.assertEquals(c.contato_ent(), u'GTECH, SAC')


