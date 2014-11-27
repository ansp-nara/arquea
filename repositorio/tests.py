# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase, client
from datetime import date

from repositorio.models import Tipo, Estado, Anexo, Repositorio, Natureza
from patrimonio.models import Tipo as TipoPatrimonio, Patrimonio
from membro.models import Membro

class RepositorioTest(TestCase):
    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml',]

    def setUp(self):
        tipoPatr = TipoPatrimonio.objects.create(nome='roteador')
        Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400", checado=True)

        tipoPatrFilho = TipoPatrimonio.objects.create(nome='placa')
        Patrimonio.objects.create(ns='kjfd1234cdf', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe", checado=True)

        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')


    def test_save__numero_sequencial(self):
        tipo = Tipo.objects.create()
        estado = Estado.objects.create()
        natureza = Natureza.objects.create(nome="problema")
		
        responsavel = Membro.objects.create(nome='Antonio')
		
        repositorio1 = Repositorio.objects.create(data_ocorrencia=date(2014,2,10), tipo=tipo, estado=estado, ocorrencia=u'Ocorrência de teste número 1', responsavel=responsavel, natureza=natureza)
        repositorio2 = Repositorio.objects.create(data_ocorrencia=date(2014,2,13), tipo=tipo, estado=estado, ocorrencia=u'Ocorrência de teste número 2', responsavel=responsavel, natureza=natureza)
		
        self.assertEqual(repositorio1.numero + 1, repositorio2.numero)


    def test_view__filtra_patrimonio(self):
        
        url = reverse("repositorio.views.ajax_seleciona_patrimonios")
        response = self.client.get(url, {'string':'3456'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"ns": "AF345678GB3489X"')


    