# -*- coding: utf-8 -*-
from django.test import TestCase, client
from repositorio.models import Tipo, Estado, Anexo, Repositorio
from datetime import date
from membro.models import Membro

# Create your tests here.

class RepositorioTest(TestCase):
	
	def setUp(self):
        tipoPatr = Tipo.objects.create(nome='roteador')
        Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)

        tipoPatr = Tipo.objects.create(nome='placa')
        Patrimonio.objects.create(ns='kjfd1234cdf', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe", checado=True)

	
	def test_save__numero_sequencial(self):
		tipo = Tipo()
		tipo.save()
		estado = Estado()
		estado.save()
		
		responsavel = Membro.objects.get(nome__startswith='Antonio')
		
		repositorio1 = Repositorio(data_ocorrencia=date(2014,2,10), tipo=tipo, estado=estado, ocorrencia=u'Ocorrência de teste número 1', responsavel=responsavel)
		repositorio2 = Repositorio(data_ocorrencia=date(2014,2,13), tipo=tipo, estado=estado, ocorrencia=u'Ocorrência de teste número 2', responsavel=responsavel)
		repositorio1.save()
		repositorio2.save()
		
		self.assertEqual(repositorio1.numero + 1, repositorio2.numero)
		
	def test_view__filtra_patrimonio(self):
		c = client.Client()
		response = c.post('/login/', {'username':'teste', 'password':'abc123'})
		self.assertEqual(response.status_code, 200)
		
		response = c.get('/repositorio/seleciona_patrimonios', {'string':'3456'})
		self.assertEqual(response.status_code, 200)
		
