# -*- coding: utf-8 -*-

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from patrimonio.models import HistoricoLocal 

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HistoricoLocalTest(TestCase):
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
        
