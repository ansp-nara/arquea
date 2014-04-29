# -*- coding: utf-8 -*-

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from datetime import date, timedelta, datetime

from patrimonio.models import HistoricoLocal, Tipo, Patrimonio, Equipamento, Estado
from patrimonio.views import *

from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
from protocolo.models import Estado as EstadoProtocolo
from identificacao.models import Entidade, Contato, Endereco, Identificacao, TipoDetalhe
from membro.models import Membro
from outorga.models import Termo


import re
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HistoricoLocalTest(TestCase):
    def test_criacao_historico_local(self):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        tipoPatr = Tipo.objects.create(nome='roteador')
        rt = Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)
        est = Estado.objects.create()
        hl = HistoricoLocal.objects.create(patrimonio=rt, endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est)

        self.assertEquals(u'05/02/2009 - NetIron400 - AF345678GB3489X -  | SAC - Dr. Ovidio, 215 - ', hl.__unicode__())


    def test_posicao_furo(self):
        """
        Teste de posicionamento de um equipamento em um furo de um rack
        """
        historico = HistoricoLocal(posicao="R042.F085")
        self.assertEquals(historico.posicao_furo, 85)
        
        historico = HistoricoLocal(posicao="P042.F017")
        self.assertEquals(historico.posicao_furo, 17)
        
        historico = HistoricoLocal(posicao="S042.F040")
        self.assertEquals(historico.posicao_furo, 40)
        
        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEquals(historico.posicao_furo, 49)
        
        historico = HistoricoLocal(posicao="60")
        self.assertEquals(historico.posicao_furo, 60)
        
        historico = HistoricoLocal(posicao="")
        self.assertEquals(historico.posicao_furo, -1)
        
        historico = HistoricoLocal()
        self.assertEquals(historico.posicao_furo, -1)
        
        historico = HistoricoLocal(posicao="S042.F049-TD")
        self.assertEquals(historico.posicao_furo, 49)

        historico = HistoricoLocal(posicao="S042.F049.TD")
        self.assertEquals(historico.posicao_furo, 49)
        
        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEquals(historico.posicao_furo, -1)
        
        historico = HistoricoLocal(posicao="S042.F001")
        self.assertEquals(historico.posicao_furo, 1)

        
    def test_posicao_colocacao(self):
        """
        Teste de colocaçao de um equipamento relativo ao furo
        Pode ser traseiro, lateral, piso
        """
        historico = HistoricoLocal(posicao="R042.F085.TD")
        self.assertEquals(historico.posicao_colocacao, 'TD')
        
        historico = HistoricoLocal(posicao="P042.F017-TD")
        self.assertEquals(historico.posicao_colocacao, 'TD')
        
        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEquals(historico.posicao_colocacao, 'piso')
        
        historico = HistoricoLocal(posicao="S042-piso")
        self.assertEquals(historico.posicao_colocacao, 'piso')
        
        historico = HistoricoLocal(posicao="60")
        self.assertEquals(historico.posicao_colocacao, None)
                
        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEquals(historico.posicao_colocacao, None)
        
        historico = HistoricoLocal(posicao="")
        self.assertEquals(historico.posicao_colocacao, None)
        
        historico = HistoricoLocal()
        self.assertEquals(historico.posicao_colocacao, None)
        

        
    def test_posicao_rack(self):
        historico = HistoricoLocal(posicao="R042.F085.TD")
        self.assertEquals(historico.posicao_rack_letra, 'R')
        self.assertEquals(historico.posicao_rack_numero, '042')
        
        historico = HistoricoLocal(posicao="P042.F017-TD")
        self.assertEquals(historico.posicao_rack_letra, 'P')
        self.assertEquals(historico.posicao_rack_numero, '042')
        
        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEquals(historico.posicao_rack_letra, 'S')
        self.assertEquals(historico.posicao_rack_numero, '042')
        
        historico = HistoricoLocal(posicao="S042-piso")
        self.assertEquals(historico.posicao_rack_letra, 'S')
        self.assertEquals(historico.posicao_rack_numero, '042')
        
        historico = HistoricoLocal(posicao="60")
        self.assertEquals(historico.posicao_rack_letra, None)
        self.assertEquals(historico.posicao_rack_numero, None)
                
        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEquals(historico.posicao_rack_letra, 'S')
        self.assertEquals(historico.posicao_rack_numero, '042')                

        historico = HistoricoLocal(posicao="AB42.F049")
        self.assertEquals(historico.posicao_rack_letra, 'AB')
        self.assertEquals(historico.posicao_rack_numero, '42')      
        
        historico = HistoricoLocal(posicao="ABC42.F049")
        self.assertEquals(historico.posicao_rack_letra, 'ABC')
        self.assertEquals(historico.posicao_rack_numero, '42')
        
    def test_posicao_rack(self):
        historico = HistoricoLocal(posicao="R042.F085.TD")
        self.assertEquals(historico.posicao_rack, 'R042')
        
        historico = HistoricoLocal(posicao="P042.F017-TD")
        self.assertEquals(historico.posicao_rack, 'P042')
        
        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEquals(historico.posicao_rack, 'S042')
        
        historico = HistoricoLocal(posicao="S042-piso")
        self.assertEquals(historico.posicao_rack, 'S042')
        
        historico = HistoricoLocal(posicao="60")
        self.assertEquals(historico.posicao_rack, None)
                
        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEquals(historico.posicao_rack, 'S042')

        historico = HistoricoLocal(posicao="AB42.F049")
        self.assertEquals(historico.posicao_rack, 'AB42')
        
        historico = HistoricoLocal(posicao="ABC42.F049")
        self.assertEquals(historico.posicao_rack, 'ABC42')

class ViewTest(TestCase):
    def setUpPatrimonio(self, num_documento='', ns=''):
        protocolo = Protocolo.objects.create(id=1, num_documento=num_documento, tipo_documento_id=0, estado_id=0, termo_id=0, data_chegada=date(year=2000, month=01, day=01), moeda_estrangeira=False)
        pagamento = Pagamento.objects.create(id=1, protocolo=protocolo, valor_fapesp=0)
        tipoPatr = Tipo.objects.create(id=1)
        patrimonio = Patrimonio.objects.create(id=1, pagamento=pagamento, tipo=tipoPatr, checado=True)
        patrimonio = Patrimonio.objects.create(id=2, ns=ns, tipo=tipoPatr, checado=True)
        
    def test_escolhe_patrimonio_ajax_empty(self):
        """
        Verifica chamanda do escolhe_patrimonio com a base vazia
        """
        url = reverse("patrimonio.views.escolhe_patrimonio")
        response = self.client.post(url)
        self.assertIn(b'Nenhum registro', response.content)

    def test_escolhe_patrimonio_ajax_not_found(self):
        """
        Verifica chamanda do escolhe_patrimonio sem encontrar registro
        """
        self.setUpPatrimonio('1134', '')
        url = reverse("patrimonio.views.escolhe_patrimonio")
        response = self.client.post(url, {'num_doc': '789'})
        self.assertIn(b'Nenhum registro', response.content)

    def test_escolhe_patrimonio_ajax_nf_pagamento(self):
        """
        Verifica chamanda do escolhe_patrimonio encontrando registro pelo num_documento do Protocolo
        """
        self.setUpPatrimonio('1234', '')
        url = reverse("patrimonio.views.escolhe_patrimonio")
        response = self.client.post(url, {'num_doc': '1234'})
        self.assertIn(b'"pk": 1', response.content)

    def test_escolhe_patrimonio_ajax_ns_patrimonio(self):
        """
        Verifica chamanda do escolhe_patrimonio encontrando registro pelo numero de serie do Patrimonio
        """
        self.setUpPatrimonio('', '7890')
        url = reverse("patrimonio.views.escolhe_patrimonio")
        response = self.client.post(url, {'num_doc': '789'})
        self.assertIn(b'"pk": 2', response.content)
        



