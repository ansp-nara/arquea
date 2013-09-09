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
from membro.models import Controle, Membro, Ferias, ControleFerias, \
    DispensaLegal, TipoDispensa
from protocolo.models import Feriado
import calendar

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FeriadoTest(TestCase):
    def test_controle_permanencia_um_dia(self):
        """
        Teste de permanencia para um dia com almoço normal de uma hora
        """
        feriado = Feriado(feriado=date(year=2000, month=01, day=01))
        feriado.save()
    
        self.assertEquals(feriado.dia_de_feriado(date(year=2000, month=01, day=01)), True)
        self.assertEquals(feriado.dia_de_feriado(date(year=2000, month=01, day=02)), False)