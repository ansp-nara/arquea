# -*- coding: utf-8 -*-

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import date, timedelta, datetime
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
import calendar
from membro.models import Controle, Membro, Ferias, ControleFerias, SindicatoArquivo, \
    DispensaLegal, TipoDispensa, Usuario, Historico, Cargo, Banco, DadoBancario, Assinatura, TipoAssinatura
from protocolo.models import Feriado
from identificacao.models import Entidade

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TipoAssinaturaTest(TestCase):
    def test_unicode (self):
        ta, created = TipoAssinatura.objects.get_or_create(nome='Cheque')
        self.assertEquals(u'Cheque', ta.__unicode__())

class UsuarioTest(TestCase):
    def test_unicode(self):
        ent = Entidade(sigla='ANSP', nome='Academic Network at São Paulo', cnpj='', fisco=True )
        ent.save()
        mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', defaults={'email': 'soraya@gomes.com', 'cpf': '000.000.000-00'})
        usr, created = Usuario.objects.get_or_create(membro=mb, username='soraya', sistema='Administrativo')

        self.assertEquals('soraya', usr.__unicode__())

class MembroTest(TestCase):
    def setUp(self):
        ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome':'Academic Network at São Paulo', 'cnpj':'', 'fisco':True})

        mb = Membro(nome='Joice Gomes', email='soraya@gomes.com', cpf='000.000.000-00', ramal=23)
        mb.save()
        
        cg = Cargo(nome='Secretaria')
        cg.save()

        ht = Historico(inicio=datetime(2008,1,1), cargo=cg, membro=mb)
        ht.save()
    
    def test_cargo_atual(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals('Secretaria', mb.cargo_atual())
    
    
    def test_cargo_atual_depois_do_desligamento(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        ht = Historico.objects.get(pk=1)
        ht.termino=datetime(2008,1,2)
        ht.save()
        
        self.assertEquals('', mb.cargo_atual())

    def test_ramal(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals(23, mb.existe_ramal())
    
    def test_curriculo_vazio(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals('', mb.existe_curriculo())

    def test_unicode(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        self.assertEquals('Joice Gomes (Secretaria)', mb.__unicode__())
        
    def test_unicode_depois_do_desligamento(self):
        mb = Membro.objects.get(email='soraya@gomes.com')
        ht = Historico.objects.get(pk=1)
        ht.termino=datetime(2008,1,2)
        ht.save()
        
        self.assertEquals('Joice Gomes', mb.__unicode__())


class DadoBancarioTest(TestCase):
    def setUp(self):
        mb = Membro(nome='Joice Gomes', funcionario=True, email='soraya@gomes.com', cpf='000.000.000-00', ramal=23)
        mb.save()
        
        cg = Cargo(nome='Secretaria')
        cg.save()

        ht = Historico(inicio=datetime(2008,1,1), cargo=cg, membro=mb)
        ht.save()

        b = Banco(numero=151, nome='Nossa Caixa')
        b.save()

        db, created = DadoBancario.objects.get_or_create(membro=mb, banco=b, agencia=1690, ag_digito=4, conta=123439, cc_digito='x')
        
        
    def test_agencia_digito(self):
        db = DadoBancario.objects.get(agencia=1690)
        self.assertEquals('1690-4',db.agencia_digito())

    def test_conta_digito(self):
        db = DadoBancario.objects.get(agencia=1690)
        self.assertEquals('123439-x', db.conta_digito())


class AssinaturaTest(TestCase):
    def setUp(self):
        mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', defaults={'email': 'soraya@gomes.com', 'cpf': '312.617.028-00'})
        ta, created = TipoAssinatura.objects.get_or_create(nome='Cheque')
        a, created = Assinatura.objects.get_or_create(membro=mb, tipo_assinatura=ta)

    def test_unicode(self):
        assinatura = Assinatura.objects.get(pk=1)
        self.assertEquals(u'Soraya Gomes | Cheque', assinatura.__unicode__())

class MembroControleTest(TestCase):
    def test_controle_permanencia_um_dia(self):
        """
        Teste de permanencia para um dia com almoço normal de uma hora
        """
        membro = Membro(nome='teste')
        controle = Controle(membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=9), 
                            almoco_devido=True, almoco=60)
        self.assertEquals(controle.segundos, 8 * 60 * 60, 'Deveria ser 28800 mas e ' + str(controle.segundos))

    def test_controle_permanencia_um_dia_almoco_menor(self):
        """
        Teste de permanencia para um dia com almoço de meia hora
        """
        membro = Membro(nome='teste')
        controle = Controle(membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=9), 
                            almoco_devido=True, almoco=30)
        self.assertEquals(controle.segundos, 8.5 * 60 * 60, 'Deveria ser 28800 mas e ' + str(controle.segundos))


    def test_controle_permanencia_sem_almoco(self):
        """
        Teste de permanencia em um dia sem almoco
        """
        membro = Membro(nome='teste')
        controle = Controle(membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=9), 
                            almoco_devido=False, almoco=60)
        self.assertEquals(controle.segundos, 9 * 60 * 60, 'Deveria ser 32400 mas e ' + str(controle.segundos))
        

    def test_controle_permanencia_sem_almoco(self):
        """
        Teste de permanencia em um dia sem almoco
        """
        membro = Membro(id=1, nome='teste')
        membro.save()
        
        controle = Controle(id=1, membro=membro, entrada=timezone.now(), saida=timezone.now()+timedelta(hours=48), 
                            almoco_devido=False, almoco=60)
        controle.save()
        
        controle = Controle.objects.get(id=1)
        
        #self.assertEquals(controle.segundos, 48 * 60 * 60)

    def test_controle_mover_bloco(self):
        membro = Membro(id=1, nome='teste')
        membro.save()
        
        controle = Controle(id=1, membro=membro, entrada=datetime(year=2000, month=01, day=01, hour=12), saida=datetime(year=2000, month=01, day=01, hour=18, minute=30), 
                            almoco_devido=False, almoco=60)
        controle.save()
        controle = Controle.objects.get(id=1)
        
        tempo = 20

        controle = Controle.objects.get(pk=1)
        controle.entrada = controle.entrada + timedelta(minutes=tempo)
        controle.saida = controle.saida + timedelta(minutes=tempo) 
        controle.save()
        
        controle = Controle.objects.get(pk=1)
        self.assertEquals(controle.entrada.month, 1)
        self.assertEquals(controle.entrada.day, 1)
        self.assertEquals(controle.entrada.hour, 12)
        self.assertEquals(controle.entrada.minute, 20)
        
        self.assertEquals(controle.saida.month, 1)
        self.assertEquals(controle.saida.day, 1)
        self.assertEquals(controle.saida.hour, 18)
        self.assertEquals(controle.saida.minute, 50)



class MembroControleHorarioTest(TestCase):
    
    def create_ferias(self, ano_corrente, mes_corrente, ferias_data_inicio, ferias_data_fim):
        mes_corrente_ini = date(ano_corrente, mes_corrente, 01)
        mes_corrente_fim = date(ano_corrente, mes_corrente, 01) + timedelta(calendar.monthrange(ano_corrente, mes_corrente)[1])
        
        membro = Membro(id=1)
        ferias = Ferias(membro = membro, id=1)
        c = ControleFerias(ferias = ferias, inicio = ferias_data_inicio, termino = ferias_data_fim, dias_uteis_fato=30, dias_uteis_aberto=0)
        c.save()
        
        # ferias_ini < mes_ini < ferias_fim  OR  mes_ini < ferias_ini < mes_fim
        controleFerias = ControleFerias.objects.filter(Q(inicio__lte=mes_corrente_ini, termino__gte=mes_corrente_ini) |
                                               Q(inicio__gte=mes_corrente_ini, inicio__lte=mes_corrente_fim),
                                               ferias=ferias)
        return controleFerias
    
    def test_controle_ferias_final_de_ano(self):
        ferias_ini = date(2012, 12, 30)
        ferias_fim = date(2013,01,01)
        
        controleFerias = self.create_ferias(2013, 01, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)
    
    def test_controle_ferias_inicio_de_mes(self):
        ferias_ini = date(2013, 01, 30)
        ferias_fim = date(2013, 02, 15)
        
        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)
        
            
    def test_controle_ferias_final_de_mes(self):
        ferias_ini = date(2013, 02, 25)
        ferias_fim = date(2013, 03, 15)
        
        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)
        
    def test_controle_ferias_meio_de_mes(self):
        ferias_ini = date(2013, 02, 10)
        ferias_fim = date(2013, 02, 25)
        
        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)
        
        
    def test_controle_ferias_entre_meses(self):
        ferias_ini = date(2013, 01, 15)
        ferias_fim = date(2013, 03, 15)
        
        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 1)
        
        
    def test_controle_ferias_mes_passado(self):
        ferias_ini = date(2013, 01, 15)
        ferias_fim = date(2013, 01, 30)
        
        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 0)
        
        
    def test_controle_ferias_ano_passado(self):
        ferias_ini = date(2012, 02, 10)
        ferias_fim = date(2012, 02, 15)
        
        controleFerias = self.create_ferias(2013, 02, ferias_ini, ferias_fim)

        self.assertEqual(controleFerias.count(), 0)
        
class DispensaLegalTest(TestCase):
    def test_dia_dispensa_mesmo_dia(self):
        membro = Membro(id=1)
        membro.save()
        
        tipo = TipoDispensa()
        tipo.save()
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(membro=membro, tipo=tipo, dias_corridos=1, horas=0, minutos=0, inicio_realizada=date(2013,07,19), realizada=True, inicio_direito=date(2013,07,19))
        dispensaLegal.save()
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,19))
        
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)

    def test_dia_dispensa_mesmo_dia_meio_periodo(self):
        membro = Membro(id=1)
        membro.save()
        
        tipo = TipoDispensa()
        tipo.save()
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(membro=membro, tipo=tipo, dias_corridos=0, horas=4, minutos=0, inicio_realizada=date(2013,07,19), realizada=True, inicio_direito=date(2013,07,19))
        dispensaLegal.save()
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,19))
        
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 4)
    
    def test_dia_dispensa_mesmo_dia_meio_periodo_e_meio(self):
        membro = Membro(id=1)
        membro.save()
        
        tipo = TipoDispensa()
        tipo.save()
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(membro=membro, tipo=tipo, dias_corridos=0, horas=4, minutos=30, inicio_realizada=date(2013,07,19), realizada=True, inicio_direito=date(2013,07,19))
        dispensaLegal.save()
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,19))
        
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 4.5)
    
    def test_dia_dispensa_dois_dias_meio_periodo_e_meio(self):
        membro = Membro(id=1)
        membro.save()
        
        tipo = TipoDispensa()
        tipo.save()
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(membro=membro, tipo=tipo, dias_corridos=2, horas=4, minutos=30, inicio_realizada=date(2013,07,19), realizada=True, inicio_direito=date(2013,07,19))
        dispensaLegal.save()
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,19))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,20))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,21))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 4.5)

    def test_dia_dispensa_dois_dias(self):
        membro = Membro(id=1)
        membro.save()
        
        tipo = TipoDispensa()
        tipo.save()
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(membro=membro, tipo=tipo, dias_corridos=2, inicio_realizada=date(2013,07,19), realizada=True, inicio_direito=date(2013,07,19))
        dispensaLegal.save()
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,18))
        self.assertEqual(dispensa['is_dispensa'], False)
        self.assertEqual(dispensa['horas'], 0)
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,19))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,20))
        self.assertEqual(dispensa['is_dispensa'], True)
        self.assertEqual(dispensa['horas'], 8)
        
        dispensa = DispensaLegal.objects.get(pk=1).dia_dispensa(date(2013,07,21))
        self.assertEqual(dispensa['is_dispensa'], False)
        self.assertEqual(dispensa['horas'], 0)
        
    def test_dia_dispensa_dia_diferente(self):
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=5, inicio_realizada=date(2013,07,19), realizada=True, )
        # dispensa para sexta, segunda, terca
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 1)


    def test_data_termino_realizada_fim_semana(self):
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=5, inicio_realizada=date(2013,07,19), realizada=True, )
        # dispensa para sexta, segunda, terca
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 1)
        
    def test_data_termino_realizada_sexta(self):
        # a data é uma sexta
        dispensaLegal = DispensaLegal(dias_corridos=1, inicio_realizada=date(2013,07,19), realizada=True, )
        # dispensa para sexta
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 4)
        
    def test_data_termino_realizada_meio_da_semana(self):
        # a data é uma segunda
        dispensaLegal = DispensaLegal(dias_corridos=3, inicio_realizada=date(2013,07,15), realizada=True, )
        # dispensa para segunda, terca, quarta
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 2)
        
    def test_data_termino_realizada_um_dia(self):
        # a data é uma segunda
        dispensaLegal = DispensaLegal(dias_corridos=1, inicio_realizada=date(2013,07,15), realizada=True, )
        
        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 15)
        # dispensa para segunda
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 0)
        
    def test_data_termino_realizada_zero_dia(self):
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=0, inicio_realizada=date(2013,07,15), realizada=True, )
        
        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 15)
        
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 0)
        self.assertEqual(dispensaLegal.inicio_realizada.weekday(), 0)
        
    def test_data_termino_realizada_meio_da_semana_com_feriado(self):
        f = Feriado(feriado=date(2013,07,16))
        f.save()
        
        # a data é uma segunda
        dispensaLegal = DispensaLegal(dias_corridos=3, inicio_realizada=date(2013,07,15), realizada=True, )
        
        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 17)
        
        # dispensa para segunda, terca, quarta
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 2)
        
    def test_data_termino_realizada_fim_semana_com_feriado_no_sabado(self):
        f = Feriado(feriado=date(2013,07,20))
        f.save()
        
        # a data é uma sexta-feira
        dispensaLegal = DispensaLegal(dias_corridos=3, inicio_realizada=date(2013,07,19), realizada=True, )
        # dispensa para sexta, segunda, terca
        self.assertEqual(dispensaLegal.termino_realizada.year, 2013)
        self.assertEqual(dispensaLegal.termino_realizada.month, 07)
        self.assertEqual(dispensaLegal.termino_realizada.day, 21)
        
        self.assertEqual(dispensaLegal.termino_realizada.weekday(), 6)
        
        
class FeriasTest(TestCase):
    def test_total_dias_uteis_aberto(self):
        """
        Teste de permanencia para um dia com almoço normal de uma hora
        """
        membro = Membro(id=1, nome='teste')
        membro.save()
        
        ferias = Ferias(id=10, membro=membro, inicio=datetime.now())
        ferias.save()
        
        controleFerias = ControleFerias(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=20, dias_uteis_aberto=10)
        controleFerias.save()
        controleFerias = ControleFerias(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=0, dias_uteis_aberto=30)
        controleFerias.save()
        controleFerias = ControleFerias(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=0, dias_uteis_aberto=30)
        controleFerias.save()
        controleFerias = ControleFerias(ferias=ferias, termino=datetime.now(), inicio=datetime.now(), dias_uteis_fato=30, dias_uteis_aberto=0)
        controleFerias.save()
        
        self.assertEquals(Ferias().total_dias_uteis_aberto(1), 20 * 8 * 60 * 60)


class MembroSindicatoArquivoTest(TestCase):
    def setUp(self):
        ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome':'Academic Network at São Paulo', 'cnpj':'', 'fisco':True})

        mb = Membro(nome='Joice Gomes', email='soraya@gomes.com', cpf='000.000.000-00', ramal=23)
        mb.save()
        
        arquivo = SindicatoArquivo(arquivo='/teste/arquivo.pdf', ano='2013', membro=mb)
        arquivo.save()

    def test_membro_sindicatoarquivo_unicode(self):
        
        arquivo = SindicatoArquivo.objects.get(pk=1)
        
        self.assertEquals(arquivo.__unicode__(), '2013 - /teste/arquivo.pdf')
        

