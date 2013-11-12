# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime
import calendar
from decimal import Decimal
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
from membro.models import Membro, Cargo, Historico
from membro.models import Controle, Membro, Ferias, ControleFerias, \
    DispensaLegal, TipoDispensa
from protocolo.models import Feriado, TipoDocumento, Origem, Protocolo, ItemProtocolo, Descricao, Cotacao
from protocolo.models import Estado as ProtocoloEstado
from identificacao.models import Identificacao, Contato, Entidade, Endereco
from outorga.models import Termo, Outorga, Categoria, Modalidade, Natureza_gasto
from outorga.models import Estado as OutorgaEstado

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ProtocoloTest(TestCase):
    def setUp(self):
        mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', defaults={'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})
        
        cg = Cargo(nome='Outorgado')
        cg.save()

        ht = Historico(inicio=datetime(2008,1,1), cargo=cg, membro=mb)
        ht.save()
        
        outorgaEstado = OutorgaEstado(nome='Pendente')
        outorgaEstado.save()
        
        t = Termo(ano=2008, processo=52885, digito=8, estado=outorgaEstado)
        t.save()
        
        categoria = Categoria(nome='Categoria')
        categoria.save()
        
        outorga = Outorga(data_solicitacao=datetime(2008,1,1), termino=datetime(2009,1,1), categoria=categoria, termo=t)
        outorga.save()
        
        td, created = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
        c, created = Contato.objects.get_or_create(primeiro_nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
        og, created = Origem.objects.get_or_create(nome='Motoboy')
        ent, created = Entidade.objects.get_or_create(sigla='NEXTEL', defaults={'nome': 'Nextel', 'cnpj': '', 'fisco': True, 'url': ''})
        endereco, created = Endereco.objects.get_or_create(entidade=ent)
        iden, created = Identificacao.objects.get_or_create(contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True, 'endereco':endereco})
        
        desc = Descricao(descricao='Descricao', entidade=ent)
        desc.save()
        
        protocoloEstado = ProtocoloEstado(nome='Pendente')
        protocoloEstado.save()
        
        p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=protocoloEstado, identificacao=iden, data_chegada=datetime(2008,9,30,10,10), \
                      data_validade=datetime(2009,8,25), data_vencimento=datetime(2008,9,30), descricao="Conta mensal", origem=og, valor_total=None, \
                      descricao2=desc)
        p.save()
        ip = ItemProtocolo(protocolo=p, descricao='Folha de pagamento', quantidade=2, valor_unitario=10000)
        ip.save()



    def test_doc_num(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('Nota Fiscal 2008', p.doc_num()) 

    def test_recebimento(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('30/09/08 10:10', p.recebimento())
# 
    def test_vencimento(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('30/09/08', p.vencimento())
        
    def test_validade(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('25/08/09', p.validade())
        
    def test_colorir(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('Pendente', p.colorir())
        
    def test_pagamentos_amanha(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(True, p.pagamentos_amanha())
        
    def test_valor(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(Decimal("20000.00"), p.valor)
        
    def test_mostra_valor(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('R$ 20.000,00', p.mostra_valor())
        
    def test_entidade(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(u'NEXTEL', p.entidade())
        
    def test_unicode(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(u'30/09 - Nota Fiscal 2008 - R$ 20.000,00', p.__unicode__())
        
    def test_existe_arquivo(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(' ', p.existe_arquivo())
        
    def test_protocolos_termo(self):
        t = Termo.objects.get(ano=2008)
        p = Protocolo.protocolos_termo(t)
        self.assertEquals('[<Protocolo: 30/09 - Nota Fiscal 2008 - R$ 20.000,00>]', str(p))

class ItemProtocoloTest(TestCase):
    def setUp(self):
        td, created = TipoDocumento.objects.get_or_create(nome='Anexo 9')
        e, created = ProtocoloEstado.objects.get_or_create(nome='Pago')
        c, created = Contato.objects.get_or_create(primeiro_nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
        og, created = Origem.objects.get_or_create(nome='Sedex')

        mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', defaults={'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})
        
        cg = Cargo(nome='Outorgado')
        cg.save()

        ht = Historico(inicio=datetime(2008,1,1), cargo=cg, membro=mb)
        ht.save()
        
        outorgaEstado = OutorgaEstado(nome='Pendente')
        outorgaEstado.save()
        
        t = Termo(ano=2008, processo=52885, digito=8, estado=outorgaEstado)
        t.save()
        
        ent, created = Entidade.objects.get_or_create(sigla='UNIEMP', defaults={'nome': 'Instituto Uniemp', 'cnpj': '', 'fisco': True, 'url': ''})
        endereco, created = Endereco.objects.get_or_create(entidade=ent)
        iden, created = Identificacao.objects.get_or_create(contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True, 'endereco':endereco})
        
        desc = Descricao(descricao='Descricao', entidade=ent)
        desc.save()

        p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=e, identificacao=iden, data_chegada=datetime(2008,9,30,10,10), \
                      data_validade=date(2009,8,25), data_vencimento=date(2008,9,30), descricao="Aditivo Uniemp", origem=og, valor_total=None, \
                      descricao2=desc)
        p.save()

        ip = ItemProtocolo(protocolo=p, descricao='Servico de conexao', quantidade=1, valor_unitario='59613.59')
        ip.save()

    def test_unicode(self):
        ip = ItemProtocolo.objects.get(pk=1)
        self.assertEquals('30/09 - Anexo 9 2008 - R$ 59.613,59 | Servico de conexao', ip.__unicode__())
    
    def test_valor(self):
        ip = ItemProtocolo.objects.get(pk=1)
        self.assertEquals(Decimal("59613.59"), ip.valor)
    
    def test_mostra_valor(self):
        ip = ItemProtocolo.objects.get(pk=1)
        self.assertEquals('R$ 59.613,59', ip.mostra_valor())


class EstadoTest(TestCase):
    def test_unicode(self):
        e, created = ProtocoloEstado.objects.get_or_create(nome='Vencido')
        self.assertEquals('Vencido', e.__unicode__())


class TipoDocumentoTest(TestCase):
    def test_unicode(self):
        td, created = TipoDocumento.objects.get_or_create(nome='Oficio')
        self.assertEquals('Oficio', td.__unicode__())


class FeriadoTest(TestCase):
    def test_unicode(self):
        f = Feriado(feriado=date(2008,10,8))
        f.save()
        
        self.assertEquals('08/10/08', f.__unicode__())
        
    def test_dia_feriado(self):
        f = Feriado(feriado=date(2008,10,8))
        f.save()
        f = Feriado(feriado=date(2008,5,18))
        f.save()
        f = Feriado(feriado=date(2008,2,22))
        f.save()
    
        self.assertEquals(Feriado.dia_de_feriado(date(2008,2,22)), True)
        self.assertEquals(Feriado.dia_de_feriado(date(2008,10,8)), True)
        self.assertEquals(Feriado.dia_de_feriado(date(2008,5,18)), True)
        
        
    def test_dia_normal(self):
        f = Feriado(feriado=date(2008,2,22))
        f.save()
        
        self.assertEquals(Feriado.dia_de_feriado(date(2007,2,22)), False)
        self.assertEquals(Feriado.dia_de_feriado(date(2007,10,8)), False)
        
class CotacaoTest(TestCase):
    def setUp(self):
        mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', defaults={'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})
        
        cg = Cargo(nome='Outorgado')
        cg.save()

        ht = Historico(inicio=datetime(2008,1,1), cargo=cg, membro=mb)
        ht.save()
        
        outorgaEstado = OutorgaEstado(nome='Pendente')
        outorgaEstado.save()
        
        t = Termo(ano=2008, processo=52885, digito=8, estado=outorgaEstado)
        t.save()
        
        ent, created = Entidade.objects.get_or_create(sigla='UNIEMP', defaults={'nome': 'Instituto Uniemp', 'cnpj': '', 'fisco': True, 'url': ''})
        endereco, created = Endereco.objects.get_or_create(entidade=ent)
        
        td, created = TipoDocumento.objects.get_or_create(nome='Anexo 9')
        e, created = ProtocoloEstado.objects.get_or_create(nome='Pago')
        c, created = Contato.objects.get_or_create(primeiro_nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
        og, created = Origem.objects.get_or_create(nome='Sedex')
        iden, created = Identificacao.objects.get_or_create(contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True, 'endereco':endereco})
        
        cot = Cotacao(termo=t, tipo_documento=td, estado=e, identificacao=iden, data_chegada=datetime(2008,12,12,9,10), \
                      data_validade=date(2009,12,13), descricao='Compra de Aparelhos', origem=og, parecer='custo alto', aceito=False, entrega='confirmada')
        cot.save()
        
    def test_unicode(self):
        cot = Cotacao.objects.get(pk=1)
        self.assertEquals(u'UNIEMP - Compra de Aparelhos', cot.__unicode__())

    def existe_entrega(self):
        cot = Cotacao.objects.get(pk=1)
        self.assertEquals('confirmada', cot.existe_entrega())
        