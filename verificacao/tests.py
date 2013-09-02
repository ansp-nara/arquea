# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from patrimonio.models import Equipamento, Patrimonio, Tipo
from verificacao.models import *


class TestPatrimonioComEquipamentpoVazio(TestCase):
    """
    Testa equipamentos com part_number vazio
    """
    def test_equipamento_vazio(self):
            eq = Equipamento(id=1, part_number="", modelo="", marca="", descricao="") 
            eq.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="", modelo="m2", marca="", descricao="", tipo=tipo1, equipamento=eq)
            patr1.save()
            patr2 = Patrimonio(part_number="pn1", modelo="m2", marca="", descricao="", tipo=tipo2)
            patr2.save()
            patr3 = Patrimonio(part_number="pn1", modelo="m2", marca="", descricao="", tipo=tipo2)
            patr3.save()
            
            verficacao = VerificacaoPatrimonio()
            retorno = verficacao.equipamentoVazio()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 2)
            

            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.equipamentoVazio(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.equipamentoVazio(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
    """
    Testa patrimonio e equipamentos com part_number diferente
    """
    def test_part_number_diferente(self):
            eq1 = Equipamento(id=1, part_number="pn1", modelo="", marca="", descricao="") 
            eq1.save()
            eq2 = Equipamento(id=2, part_number="", modelo="", marca="", descricao="") 
            eq2.save()
            eq3 = Equipamento(id=3, part_number="pn3", modelo="", marca="", descricao="") 
            eq3.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="pn1", modelo="m2", marca="", descricao="", tipo=tipo1, equipamento=eq1)
            patr1.save()
            patr2 = Patrimonio(part_number="", modelo="m2", marca="", descricao="", tipo=tipo1, equipamento=eq2)
            patr2.save()
            patr3 = Patrimonio(part_number="pn11111", modelo="m2", marca="", descricao="", tipo=tipo2, equipamento=eq3)
            patr3.save()
            
            verficacao = VerificacaoPatrimonioEquipamento()
            retorno = verficacao.partNumberDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)

            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.partNumberDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.partNumberDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            
    """
    Testa patrimonio e equipamentos com descricao diferente
    """
    def test_descricao_diferente(self):
            eq1 = Equipamento(id=1, part_number="", modelo="", marca="", descricao="desc1") 
            eq1.save()
            eq2 = Equipamento(id=2, part_number="", modelo="", marca="", descricao="") 
            eq2.save()
            eq3 = Equipamento(id=3, part_number="", modelo="", marca="", descricao="desc3") 
            eq3.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="pt1", modelo="pt1", marca="m1", descricao="desc1", tipo=tipo1, equipamento=eq1)
            patr1.save()
            patr2 = Patrimonio(part_number="pt2", modelo="pt2", marca="m2", descricao="", tipo=tipo1, equipamento=eq2)
            patr2.save()
            patr3 = Patrimonio(part_number="pt3", modelo="pt3", marca="m3", descricao="desc11111", tipo=tipo2, equipamento=eq3)
            patr3.save()
            
            verficacao = VerificacaoPatrimonioEquipamento()
            retorno = verficacao.descricaoDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.descricaoDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.descricaoDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
    """
    Testa patrimonio e equipamentos com modelo diferente
    """
    def test_modelo_diferente(self):
            eq1 = Equipamento(id=1, part_number="", modelo="m1", marca="", descricao="") 
            eq1.save()
            eq2 = Equipamento(id=2, part_number="", modelo="", marca="", descricao="") 
            eq2.save()
            eq3 = Equipamento(id=3, part_number="", modelo="m3", marca="", descricao="") 
            eq3.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="pt1", modelo="m1", marca="pt1", descricao="pt1", tipo=tipo1, equipamento=eq1)
            patr1.save()
            patr2 = Patrimonio(part_number="pt2", modelo="", marca="pt2", descricao="pt2", tipo=tipo1, equipamento=eq2)
            patr2.save()
            patr3 = Patrimonio(part_number="pt3", modelo="m1111", marca="pt3", descricao="pt3", tipo=tipo2, equipamento=eq3)
            patr3.save()
            
            verficacao = VerificacaoPatrimonioEquipamento()
            retorno = verficacao.modeloDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.modeloDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.modeloDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            
    """
    Testa patrimonio e equipamentos com marca diferente
    """
    def test_marca_diferente(self):
            eq1 = Equipamento(id=1, part_number="", modelo="", marca="m1", descricao="") 
            eq1.save()
            eq2 = Equipamento(id=2, part_number="", modelo="", marca="", descricao="") 
            eq2.save()
            eq3 = Equipamento(id=3, part_number="", modelo="", marca="m3", descricao="") 
            eq3.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="pt1", modelo="pt1", marca="m1", descricao="pt1", tipo=tipo1, equipamento=eq1)
            patr1.save()
            patr2 = Patrimonio(part_number="pt2", modelo="pt2", marca="", descricao="pt2", tipo=tipo1, equipamento=eq2)
            patr2.save()
            patr3 = Patrimonio(part_number="pt3", modelo="pt3", marca="m1111", descricao="pt3", tipo=tipo2, equipamento=eq3)
            patr3.save()
            
            verficacao = VerificacaoPatrimonioEquipamento()
            retorno = verficacao.marcaDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.marcaDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.marcaDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
    """
    Testa patrimonio e equipamentos com ncm diferente
    """
    def test_ncm_diferente(self):
            eq1 = Equipamento(id=1, part_number="", modelo="", marca="", descricao="", ncm="n1") 
            eq1.save()
            eq2 = Equipamento(id=2, part_number="", modelo="", marca="", descricao="", ncm="") 
            eq2.save()
            eq3 = Equipamento(id=3, part_number="", modelo="", marca="", descricao="", ncm="n3") 
            eq3.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="pt1", modelo="pt1", marca="pt1", descricao="pt1", ncm="n1", tipo=tipo1, equipamento=eq1)
            patr1.save()
            patr2 = Patrimonio(part_number="pt2", modelo="pt2", marca="pt2", descricao="pt2", ncm="", tipo=tipo1, equipamento=eq2)
            patr2.save()
            patr3 = Patrimonio(part_number="pt3", modelo="pt3", marca="pt3", descricao="pt3", ncm="n1111", tipo=tipo2, equipamento=eq3)
            patr3.save()
            
            verficacao = VerificacaoPatrimonioEquipamento()
            retorno = verficacao.ncmDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.ncmDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.ncmDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
           
           
    """
    Testa patrimonio e equipamentos com tamanhos diferente
    """
    def test_tamanho_diferente(self):
            eq1 = Equipamento(id=1, part_number="", modelo="", marca="", descricao="", ncm="n1", tamanho=1.0) 
            eq1.save()
            eq2 = Equipamento(id=2, part_number="", modelo="", marca="", descricao="", ncm="") 
            eq2.save()
            eq3 = Equipamento(id=3, part_number="", modelo="", marca="", descricao="", ncm="n3", tamanho=1.0) 
            eq3.save()
        
            tipo1 = Tipo()
            tipo1.nome = 'tipo1'
            tipo1.save()
            tipo2 = Tipo()
            tipo2.nome = 'tipo2'
            tipo2.save()
        
            patr1 = Patrimonio(part_number="pt1", modelo="pt1", marca="pt1", descricao="pt1", ncm="n1", tamanho=1.0,  tipo=tipo1, equipamento=eq1)
            patr1.save()
            patr2 = Patrimonio(part_number="pt2", modelo="pt2", marca="pt2", descricao="pt2", ncm="", tipo=tipo1, equipamento=eq2)
            patr2.save()
            patr3 = Patrimonio(part_number="pt3", modelo="pt3", marca="pt3", descricao="pt3", ncm="n1111", tamanho=11.0, tipo=tipo2, equipamento=eq3)
            patr3.save()
            
            verficacao = VerificacaoPatrimonioEquipamento()
            retorno = verficacao.tamanhoDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
            # check filter            
            filtro = {"filtro_tipo_patrimonio":1}
            retorno = verficacao.tamanhoDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 0)
            
            patr3.tipo = tipo1;
            patr3.save()
            
            retorno = verficacao.tamanhoDiferente(filtro)
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 1)
            
    """
    Testa a copia de atributos entre patrimonio e equipamento
    """
    def test_copy_attribute(self):
            eq1 = Equipamento(id=1, part_number="", modelo="", marca="", descricao="", ncm="") 
            eq1.save()
        
            tipo = Tipo()
            tipo.save()
        
            patr = Patrimonio(id = 2, part_number="part_number1", modelo="modelo1", marca="marca1", descricao="descricao1", ncm="ncm1", tipo=tipo, equipamento=eq1)
            patr.save()
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.descricao, patr.equipamento.descricao)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('equipamento', 2, 'descricao')
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            logger.debug(eq_retrieve)
            self.assertEqual(patr_retrieve.descricao, eq_retrieve.descricao)
            self.assertEqual(eq_retrieve.descricao, 'descricao1')
            
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.part_number, patr.equipamento.part_number)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('equipamento', 2, 'part_number')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.part_number, eq_retrieve.part_number)
            self.assertEqual(eq_retrieve.part_number, 'part_number1')
            
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.descricao, patr.equipamento.modelo)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('equipamento', 2, 'modelo')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.modelo, eq_retrieve.modelo)
            self.assertEqual(eq_retrieve.modelo, 'modelo1')
            
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.ncm, patr.equipamento.ncm)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('equipamento', 2, 'ncm')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.ncm, eq_retrieve.ncm)
            self.assertEqual(eq_retrieve.ncm, 'ncm1')
            
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.descricao, patr.equipamento.marca)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('equipamento', 2, 'marca')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.marca, eq_retrieve.marca)
            self.assertEqual(eq_retrieve.marca, 'marca1')
            
            
  
    """
    Testa a copia de atributos entre equipamento e patrimonio
    """
    def test_copy_attribute(self):
            eq1 = Equipamento(id=1, part_number="part_number1", modelo="modelo1", marca="marca1", descricao="descricao1", ncm="ncm1") 
            eq1.save()
        
            tipo = Tipo()
            tipo.save()
        
            patr = Patrimonio(id = 2, part_number="", modelo="", marca="", descricao="", ncm="", tipo=tipo, equipamento=eq1)
            patr.save()
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.descricao, patr.equipamento.descricao)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('patrimonio', 2, 'descricao')
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.descricao, eq_retrieve.descricao)
            self.assertEqual(patr_retrieve.descricao, 'descricao1')
            
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.part_number, patr.equipamento.part_number)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('patrimonio', 2, 'part_number')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.part_number, eq_retrieve.part_number)
            self.assertEqual(patr_retrieve.part_number, 'part_number1')

            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.descricao, patr.equipamento.modelo)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('patrimonio', 2, 'modelo')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.modelo, eq_retrieve.modelo)
            self.assertEqual(patr_retrieve.modelo, 'modelo1')

            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.ncm, patr.equipamento.ncm)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('patrimonio', 2, 'ncm')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.ncm, eq_retrieve.ncm)
            self.assertEqual(patr_retrieve.ncm, 'ncm1')
            
            
            # verifica se o valor do atributo está diferente ANTES do teste
            self.assertNotEqual(patr.descricao, patr.equipamento.marca)
            verficacao = VerificacaoPatrimonioEquipamento()
            verficacao.copy_attribute('patrimonio', 2, 'marca')
            # verifica se o valor do atributo está diferente DEPOIS do teste
            patr_retrieve = Patrimonio.objects.get(pk=2)
            eq_retrieve = Equipamento.objects.get(pk=1)
            self.assertEqual(patr_retrieve.marca, eq_retrieve.marca)
            self.assertEqual(patr_retrieve.marca, 'marca1')
            

class TestEquipamentoPNvVazio(TestCase):
    """
    Testa equipamentos com part_number vazio e com modelo vazio
    """
    def test_pn_vazio(self):
            eq = Equipamento(part_number="", modelo="", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="", modelo="", marca="marca", descricao="")
            eq.save()
            eq = Equipamento(part_number="", modelo="m2", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="pn1", modelo="m2", marca="", descricao="")
            eq.save()
            
            verficacao = VerificacaoEquipamento()
            retorno = verficacao.partNumberVazioModeloVazio()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 2)

class TestEquipamentoPNvsModelo(TestCase):
    
    # teste sem nenhum pn duplicado mas sem modelos diferentes
    def test_sem_pn_duplicados(self):
        
        eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn2", modelo="m2", marca="", descricao="")
        eq.save()
        
        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()
        
        self.assertEqual(len(retorno), 0)


    # teste com dois PN duplicados mas sem modelos diferentes
    def test_com_multiplos_pn_duplicados(self):
        eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
        eq.save()
        eq.save()
        eq = Equipamento(part_number="pn2", modelo="m2", marca="", descricao="")
        eq.save()
        
        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()
        
        self.assertEqual(len(retorno), 0)
        
    # teste com dois PN duplicados mas sem modelos diferentes
    def test_com_dois_pn_duplicados(self):
        eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn2", modelo="m2", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn2", modelo="m2", marca="", descricao="")
        eq.save()
        
        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()
        
        self.assertEqual(len(retorno), 0)
    
        
    # teste com dois PN duplicados mas com modelos diferentes
    def test_com_dois_pn_modelos_duplicados_diferentes(self):
        eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn1", modelo="m2", marca="", descricao="")
        eq.save()
        eq = Equipamento(part_number="pn1", modelo="m2", marca="", descricao="")
        eq.save()
        
        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()
        
        self.assertEqual(len(retorno[0]), 3)
        
    # teste com dois PN duplicados mas com modelos diferentes
    def test_com_dois_pn_modelos_diferentes(self):
            eq = Equipamento(part_number="pn1", modelo="m1", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="pn1", modelo="m2", marca="", descricao="")
            eq.save()
            
            verficacao = VerificacaoEquipamento()
            retorno = verficacao.partNumberVSModeloDiferente()
            
            self.assertEqual(len(retorno[0]), 2)
            
    # teste com dois PN vazio
    def test_com_dois_pn_modelos_diferentes(self):
            eq = Equipamento(part_number="", modelo="m1", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="", modelo="m2", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="", modelo="m2", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="p1", modelo="m2", marca="", descricao="")
            eq.save()
            eq = Equipamento(part_number="p1", modelo="m1", marca="", descricao="")
            eq.save()
            
            verficacao = VerificacaoEquipamento()
            retorno = verficacao.partNumberVSModeloDiferente()
            
            self.assertEqual(len(retorno), 1)
            self.assertEqual(len(retorno[0]), 2)


