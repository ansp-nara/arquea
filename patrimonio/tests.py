# -*- coding: utf-8 -*-

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from datetime import date, timedelta, datetime

from patrimonio.models import HistoricoLocal, Tipo, Patrimonio, Equipamento, Estado, TipoEquipamento
from patrimonio.views import *
from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo, Estado as EstadoProtocolo
from identificacao.models import Entidade, Contato, Endereco, Identificacao, TipoDetalhe
from membro.models import Membro
from outorga.models import Termo, Estado as EstadoOutorga, Acordo, OrigemFapesp, Categoria, Outorga
from financeiro.models import ExtratoCC, Estado as EstadoFinanceiro, TipoComprovante, Auditoria

import re
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


class EstadoTest(TestCase):
    def test_unicode(self):
        est = Estado.objects.create(nome="ESTADO_NOME")
        
        self.assertEquals(u'ESTADO_NOME', est.__unicode__())


class TipoTest(TestCase):
    def test_unicode(self):
        tipo = Tipo.objects.create(nome="TIPO_NOME")
        
        self.assertEquals(u'TIPO_NOME', tipo.__unicode__())


class DirecaoTest(TestCase):
    def test_unicode(self):
        direcao = Direcao.objects.create(origem="ORIGEM", destino="DESTINO")
        
        self.assertEquals(u'ORIGEM - DESTINO', direcao.__unicode__())

    def test_meta(self):
        self.assertEquals(u'Direção', Direcao._meta.verbose_name)
        self.assertEquals(u'Direções', Direcao._meta.verbose_name_plural)


class DistribuicaoUnidadeTest(TestCase):
    def test_unicode(self):
        distribuicaoUnidade = DistribuicaoUnidade.objects.create(nome="NOME", sigla="SIGLA")
        
        self.assertEquals(u'SIGLA - NOME', distribuicaoUnidade.__unicode__())

class DistribuicaoTest(TestCase):
    def test_unicode(self):
        distribuicaoUnidade = DistribuicaoUnidade.objects.create(nome="NOME", sigla="SIGLA")
        direcao = Direcao.objects.create(origem="ORIGEM", destino="DESTINO")
        distribuicao = Distribuicao.objects.create(inicio=1, final=2, unidade=distribuicaoUnidade, direcao=direcao)
        
        self.assertEquals(u'1 - 2', distribuicao.__unicode__())


class UnidadeDimensaoTest(TestCase):
    def test_unicode(self):
        unidadeDimensao = UnidadeDimensao.objects.create(nome="NOME")
        
        self.assertEquals(u'NOME', unidadeDimensao.__unicode__())

    def test_meta(self):
        self.assertEquals(u'Unidade da dimensão', UnidadeDimensao._meta.verbose_name)
        self.assertEquals(u'Unidade das dimensões', UnidadeDimensao._meta.verbose_name_plural)



class DimensaoTest(TestCase):
    def test_unicode(self):
        unidadeDimensao = UnidadeDimensao.objects.create(nome="UNIDADE")
        dimensao = Dimensao.objects.create(altura=1, largura=2, profundidade=3, peso=4, unidade=unidadeDimensao)
        
        self.assertEquals(u'1 x 2 x 3 UNIDADE - 4 kg', dimensao.__unicode__())

    def test_meta(self):
        self.assertEquals(u'Dimensão', Dimensao._meta.verbose_name)
        self.assertEquals(u'Dimensões', Dimensao._meta.verbose_name_plural)


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
        

        
    def test_posicao_rack__letra_numero(self):
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


class PatrimonioTest(TestCase):
    def setUp(self):
        tipoPatr = Tipo.objects.create(nome='roteador')
        tipoEquipamento = TipoEquipamento.objects.create(nome="Rack")
        entidade_fabricante = Entidade.objects.create(sigla='DELL', nome='Dell', cnpj='00.000.000/0000-00', fisco=True, url='')
        entidade_procedencia = Entidade.objects.create(sigla='PROC', nome='Entidade_Procedencia', cnpj='00.000.000/0000-00', fisco=True, url='')
        equipamento = Equipamento.objects.create(tipo=tipoEquipamento, part_number="PN001", modelo="MODEL001", ncm="NCM001", \
                                                 ean="EAN001", entidade_fabricante=entidade_fabricante)
        
        rt = Patrimonio.objects.create(equipamento=equipamento, ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, \
                                       apelido="NetIron400", checado=True, entidade_procedencia=entidade_procedencia)

    def _setUpHistorico(self, patrimonio):
        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        hl = HistoricoLocal.objects.create(patrimonio=patrimonio, endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est, posicao='S042')
        hl = HistoricoLocal.objects.create(patrimonio=patrimonio, endereco= endDet, descricao='Emprestimo 2', data= datetime.date(2010,2,5), estado=est, posicao='S043')
        
        
    def test_historico_atual(self):
        """
        Verifica chamanda do historico atual do patrimonio
        """
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self._setUpHistorico(patr)

        hist = patr.historico_atual
        self.assertEquals('Emprestimo 2', hist.descricao)
        
    def test_historico_atual_vazio(self):
        """
        Verifica chamanda do historico atual do patrimonio
        """
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')

        hist = patr.historico_atual
        self.assertIsNone(hist)

    def test_historico_atual_prefetched(self):
        """
        Verifica chamanda do historico atual do patrimonio
        """
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self._setUpHistorico(patr)
        hist = patr.historico_atual
        self.assertEquals('Emprestimo 2', hist.descricao)


    def test_marca(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        marca = patr.marca
        self.assertEquals('DELL', marca)


    def test_marca_vazia(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento.entidade_fabricante.sigla = None
        self.assertEquals('', patr.marca)
        
        patr.equipamento.entidade_fabricante = None
        self.assertEquals('', patr.marca)
        
        patr.equipamento = None
        self.assertEquals('', patr.marca)


    def test_modelo(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        modelo = patr.modelo
        self.assertEquals('MODEL001', modelo)

    def test_modelo_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento = None
        self.assertEquals('', patr.modelo)

    def test_part_number(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        part_number = patr.part_number
        self.assertEquals('PN001', part_number)
    
    def test_part_number_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento = None
        self.assertEquals('', patr.part_number)

    def test_ean(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        ean = patr.ean
        self.assertEquals('EAN001', ean)

    def test_ean_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento = None
        self.assertEquals('', patr.ean)

    def test_procedencia(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        procedencia = patr.procedencia
        self.assertEquals('PROC', procedencia)

    def test_procedencia_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.entidade_procedencia = None
        self.assertEquals('', patr.procedencia)

    def test_posicao(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self._setUpHistorico(patr)
        self.assertEquals(' - S043', patr.posicao())

    def test_posicao_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self.assertEquals('', patr.posicao())

    def test_nf(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        
        protocolo = Protocolo.objects.create(id=1, num_documento='00001', tipo_documento_id=0, estado_id=0, termo_id=0, data_chegada=date(year=2000, month=01, day=01), moeda_estrangeira=False)
        pagamento = Pagamento.objects.create(id=1, protocolo=protocolo, valor_fapesp=0)
        patr.pagamento = pagamento
        
        self.assertEquals('00001', patr.nf())

    def test_nf_vazio_pagamento_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.pagamento = None
        
        self.assertEquals('', patr.nf())

    def test_auditoria(self):
        #Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008,1,1), estado=e)
        #Cria Outorga
        c1 = Categoria.objects.create()
        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007,12,1), termino=date(2008,12,31), data_presta_contas=date(2008,2,28))

        #Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB', )
        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')

        #Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', cnpj='00.000.000/0000-00', fisco=True, url='')
        end1 = Endereco.objects.create(entidade=ent1)
        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, quantidade=12, valor=2500)

        #Cria Protocolo
        ep = EstadoProtocolo.objects.create()
        td = TipoDocumento.objects.create()
        og = Origem.objects.create()
        cot1 = Contato.objects.create()
        
        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, ativo=True)
        
        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=date(2008,9,30), \
                                      origem=og, estado=ep, num_documento=8888)

        #Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create()
        ex1 = ExtratoCC.objects.create(data_extrato=date(2008,10,30), data_oper=date(2008,10,5), cod_oper=333333, valor='2650', historico='TED', despesa_caixa=False)
        a1 = Acordo.objects.create(estado=ef1)
        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')
        
        efi1 = EstadoFinanceiro.objects.create()
        tcomprov1 = TipoComprovante.objects.create()

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=fp1, tipo=tcomprov1, parcial=101.0, pagina=102.0, obs='observacao')

        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.pagamento = fp1
        
        self.assertEquals('STB (101/102)', patr.auditoria())

    def test_auditoria_vazia(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.pagamento = None
        
        self.assertEquals('', patr.auditoria())


    def nf(self):
        if self.pagamento is not None and self.pagamento.protocolo is not None:
            return u'%s' % self.pagamento.protocolo.num_documento
        else:
            return ''



class ViewTest(TestCase):
 
    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml',]
    
    def setUp(self):
        super(ViewTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

        
    def setUpPatrimonio(self, num_documento='', ns=''):
        protocolo = Protocolo.objects.create(id=1, num_documento=num_documento, tipo_documento_id=0, estado_id=0, termo_id=0, data_chegada=date(year=2000, month=01, day=01), moeda_estrangeira=False)
        pagamento = Pagamento.objects.create(id=1, protocolo=protocolo, valor_fapesp=0)
        tipoPatr = Tipo.objects.create(id=1)
        patr1 = Patrimonio.objects.create(id=1, pagamento=pagamento, tipo=tipoPatr, checado=True)
        patr2 = Patrimonio.objects.create(id=2, ns=ns, tipo=tipoPatr, checado=True)

        ent= Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True, url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create(nome="Ativo")
        hl = HistoricoLocal.objects.create(patrimonio=patr1, endereco= endDet, descricao='Emprestimo', data= datetime.date(2009,2,5), estado=est, posicao='S042')

    
    def test_escolhe_patrimonio_ajax_empty(self):
        """
        Verifica chamanda do escolhe_patrimonio com a base vazia
        """
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        self.response = self.client.get(url)
        self.assertTrue(200, self.response.status_code)
        
        self.assertIn(b'Nenhum registro', self.response.content)


    def test_escolhe_patrimonio_ajax_not_found(self):
        """
        Verifica chamanda do escolhe_patrimonio sem encontrar registro
        """
        self.setUpPatrimonio('1134', '')
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        response = self.client.get(url, {'num_doc': '789'})
        self.assertIn(b'Nenhum registro', response.content)


    def test_escolhe_patrimonio_ajax_nf_pagamento(self):
        """
        Verifica chamanda do escolhe_patrimonio encontrando registro pelo num_documento do Protocolo
        """
        self.setUpPatrimonio('1234', '')
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        response = self.client.get(url, {'num_doc': '1234'})
        self.assertIn(b'"pk": 1', response.content)

    def test_escolhe_patrimonio_ajax_ns_patrimonio(self):
        """
        Verifica chamanda do escolhe_patrimonio encontrando registro pelo numero de serie do Patrimonio
        """
        self.setUpPatrimonio('', '7890')
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        response = self.client.get(url, {'num_doc': '789'})
        self.assertIn(b'"pk": 2', response.content)
        
    def test_por_estado(self):
        """
        View por estado.
        """
        self.setUpPatrimonio()
        
        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url, {'estado': '1'})
        
        self.assertTrue(200, response.status_code)
        self.assertContains(response, '<h4>Estado Ativo</h4>')
        self.assertContains(response, '/admin/patrimonio/patrimonio/1/')
        
        
    def test_por_estado__parametro_estado_vazio(self):
        """
        View por estado. 
        Sem o envio de parametro de estado, deve ir para a tela de filtro de seleção do estado.
        """
        self.setUpPatrimonio()
        
        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url)
        
        self.assertTrue(200, response.status_code)
        self.assertContains(response, '<option value="1">Ativo (1)</option>')
    
    def test_ajax_patrimonio_historico(self):
        """
        View por estado.
        """
        self.setUpPatrimonio()
        
        url = reverse("patrimonio.views.ajax_patrimonio_historico")
        response = self.client.get(url, {'id': '1'})
                
        self.assertTrue(200, response.status_code)
        
        self.assertContains(response, '"estado_desc": "Ativo"')
        self.assertContains(response, '"entidade_id": 1')
        self.assertContains(response, '"estado_id": 1')
        self.assertContains(response, '"localizacao_id": 1')
        self.assertContains(response, '"data": "2014-11-27"') 
        self.assertContains(response, '"entidade_desc": "SAC"')
        self.assertContains(response, '"descricao": "Emprestimo"')
        self.assertContains(response, '"posicao": "S042"')
        self.assertContains(response, '"localizacao_desc": "SAC - Dr. Ovidio, 215 - "')
        
    

class ViewPermissionDeniedTest(TestCase):
    """
    Teste das permissões das views. Utilizando um usuário sem permissão de superusuário.
    """
    fixtures = ['auth_user.yaml',]
    
    def setUp(self):
        super(ViewPermissionDeniedTest, self).setUp()
        self.response = self.client.login(username='john', password='123456')

    def test_por_estado(self):
        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url)
        self.assertContains(response, '403 Forbidden', status_code=403)
    
    
class ViewParcialPermissionTest(TestCase):
    """
    Teste das permissões das views. Utilizando um usuário com permissão individual por view.
    """
    fixtures = ['auth_user_patrimonio_permission.yaml',]
    
    def setUp(self):
        super(ViewParcialPermissionTest, self).setUp()
        self.response = self.client.login(username='paul', password='123456')

    def test_por_estado(self):
        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url)
        self.assertContains(response, 'breadcrumbs', status_code=200)
    
    