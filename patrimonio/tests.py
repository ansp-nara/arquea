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
    def test_posicao_int(self):
        """
        Teste de permanencia para um dia com almoço normal de uma hora
        """
        historico = HistoricoLocal(posicao="R042.F085")
        self.assertEquals(historico.posicao_int, 85)
        
        historico = HistoricoLocal(posicao="P042.F017")
        self.assertEquals(historico.posicao_int, 17)
        
        historico = HistoricoLocal(posicao="S042.F040")
        self.assertEquals(historico.posicao_int, 40)
        
        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEquals(historico.posicao_int, 49)
        
        historico = HistoricoLocal(posicao="60")
        self.assertEquals(historico.posicao_int, 60)
        
        
        
