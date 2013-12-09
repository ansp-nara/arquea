# -*- coding: utf-8 -*-
from django.test import TestCase
import mock
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UnitTestCase(TestCase):
    """
    Classe para utilização em testes unitários.
    """
