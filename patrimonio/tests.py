# -*- coding: utf-8 -*-

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.core.urlresolvers import resolve
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


class PatrimonioTest(TestCase):
    
    def test_save___historico_do_filho__posicao_diferente(self):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        tipoPatr = Tipo.objects.create(nome='roteador')
        
        patrPai = Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)
        historicoPai = HistoricoLocal.objects.create(patrimonio=patrPai, posicao="R039.F001", endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrPai = Patrimonio.objects.get(pk=patrPai.pk)
        
        tipoPatrFilho = Tipo.objects.create(nome='placa')
        patrFilho = Patrimonio.objects.create(ns='NSFILHO', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe", patrimonio=patrPai, checado=True)
        historicoFilho = HistoricoLocal.objects.create(patrimonio=patrFilho, posicao="R042.F001", endereco= endDet, descricao='Emprestimo', data= datetime.date(2007,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        
        # verificando se o valor de historico ainda está diferente
        self.assertNotEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)
        patrPai.save()
        
        # verificando se o valor de historico do filho foi recarregado
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        self.assertEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)
        
    def test_save___historico_do_filho__pai_com_posicao_vazia(self):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        tipoPatr = Tipo.objects.create(nome='roteador')
        
        patrPai = Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)
        # inserindo histórico sem posição
        historicoPai = HistoricoLocal.objects.create(patrimonio=patrPai, endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrPai = Patrimonio.objects.get(pk=patrPai.pk)
        
        tipoPatrFilho = Tipo.objects.create(nome='placa')
        patrFilho = Patrimonio.objects.create(ns='NSFILHO', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe", patrimonio=patrPai, checado=True)
        historicoFilho = HistoricoLocal.objects.create(patrimonio=patrFilho, posicao="R042.F001", endereco= endDet, descricao='Emprestimo', data= datetime.date(2007,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        
        # verificando se o valor de historico ainda está diferente
        self.assertNotEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)
        patrPai.save()
        
        # verificando se o valor de historico do filho foi recarregado
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        self.assertEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)

    def test_save___historico_do_filho__filho_com_posicao_vazia(self):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        tipoPatr = Tipo.objects.create(nome='roteador')
        
        patrPai = Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)
        historicoPai = HistoricoLocal.objects.create(patrimonio=patrPai, posicao="R039.F001", endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrPai = Patrimonio.objects.get(pk=patrPai.pk)
        
        tipoPatrFilho = Tipo.objects.create(nome='placa')
        patrFilho = Patrimonio.objects.create(ns='NSFILHO', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe", patrimonio=patrPai, checado=True)
        # inserindo histórico sem posição
        historicoFilho = HistoricoLocal.objects.create(patrimonio=patrFilho,endereco= endDet, descricao='Emprestimo', data= datetime.date(2007,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        
        # verificando se o valor de historico ainda está diferente
        self.assertNotEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)
        patrPai.save()
        
        # verificando se o valor de historico do filho foi recarregado
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        self.assertEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)

    def test_save___historico_do_filho__filho_com_data_mais_atual(self):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        tipoPatr = Tipo.objects.create(nome='roteador')
        
        patrPai = Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)
        historicoPai = HistoricoLocal.objects.create(patrimonio=patrPai, posicao="R039.F001", endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrPai = Patrimonio.objects.get(pk=patrPai.pk)
        
        tipoPatrFilho = Tipo.objects.create(nome='placa')
        patrFilho = Patrimonio.objects.create(ns='NSFILHO', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe", patrimonio=patrPai, checado=True)
        # colocando uma data de histórico mais nova que o do histórico do pai
        historicoFilho = HistoricoLocal.objects.create(patrimonio=patrFilho,endereco= endDet, descricao='Emprestimo', data= datetime.date(2013,2,5), estado=est)
        # pegando novamente o objeto para resetar a propriedade do historico_atual
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        
        # verificando se o valor de historico ainda está diferente
        self.assertNotEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)
        patrPai.save()
        
        # verificando se o valor de historico do filho continua o mesmo, já que possui histórico com data mais nova que o do patrimonio pai
        patrFilho = Patrimonio.objects.get(pk=patrFilho.pk)
        self.assertNotEqual(patrPai.historico_atual.posicao, patrFilho.historico_atual.posicao)


    def test_save___historico_do_filho__endereco_diferente(self):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        tipoPatr = Tipo.objects.create(nome='roteador')


class HistoricoLocalTest(TestCase):
    def test_criacao_historico_local(self):
        ent= Entidade(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        ent.save()
        
        end = Endereco(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        end.save()
        
        tipoDetalhe = TipoDetalhe()
        tipoDetalhe.save()
        
        endDet = EnderecoDetalhe(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        endDet.save()

        tipoPatr = Tipo(nome='roteador')
        tipoPatr.save()

        rt = Patrimonio(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)
        rt.save()

        est = Estado()
        est.save()

        hl = HistoricoLocal(patrimonio=rt, endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est)
        hl.save()

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
        protocolo = Protocolo(id=1, num_documento=num_documento, tipo_documento_id=0, estado_id=0, termo_id=0, data_chegada=date(year=2000, month=01, day=01), moeda_estrangeira=False)
        protocolo.save()
        pagamento = Pagamento(id=1, protocolo=protocolo, valor_fapesp=0)
        pagamento.save()
        tipoPatr = Tipo(id=1)
        tipoPatr.save()
        patrimonio = Patrimonio(id=1, pagamento=pagamento, tipo=tipoPatr, checado=True)
        patrimonio.save()
        
        patrimonio = Patrimonio(id=2, ns=ns, tipo=tipoPatr, checado=True)
        patrimonio.save()
        
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
        



