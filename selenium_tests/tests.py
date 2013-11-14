# -*- coding: utf-8 -*-
from utils.SeleniumServerTestCase import SeleniumServerTestCase
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class HomeTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(HomeTest, self).setUp()
        
    def tearDown(self):
        super(HomeTest, self).tearDown()
    
    def test_home_page(self):
        self.browser.get(self.sistema_url + '/admin/')
         
        elemHeader = self.browser.find_element_by_css_selector('div#container h1')
        self.assertEquals(elemHeader.text, u'Administração do Site')
 
        
    def test_controle_500(self):
        req = self.browser.get(self.sistema_url + '/membro/mensalf?ano=2012&mes=1&')
        self.assertTrue(self.is_http_500(), u'Requisicao retornou HTTP (500)')
        self.assertFalse(self.is_http_404(), u'Requisicao retornou HTTP (404)')
                
    def test_controle_404(self):
        self.browser.get(self.sistema_url + '/admin/asdfasdfasdf/')
        self.assertTrue(self.is_http_404(), u'Requisicao retornou HTTP (404)')
        self.assertFalse(self.is_http_500(), u'Requisicao retornou HTTP (500)')


class FinanceiroAcordosTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(FinanceiroAcordosTest, self).setUp()
        
    def tearDown(self):
        super(FinanceiroAcordosTest, self).tearDown()
    
    def test_relatorio_acordo_filtro_inicial(self):
        """
        Verifica se o filtro de acordo lista ao menos os últimos 5 acordos
        """
        self.browser.get(self.sistema_url + '/financeiro/relatorios/acordos')
         
        elem = self.browser.find_element_by_css_selector('select#id_termo')
        
        self.assertTrue(elem.text.find('13/11711-5') >= 0)
        self.assertTrue(elem.text.find('11/52044-6') >= 0)
        self.assertTrue(elem.text.find('10/52277-8') >= 0)
        self.assertTrue(elem.text.find('09/11388-4') >= 0)
        self.assertTrue(elem.text.find('08/52885-8') >= 0)
        
    def test_relatorio_acordo_conteudo(self):
        """
        Verifica se o relatorio foi aberto
        """
        self.browser.get(self.sistema_url + '/financeiro/relatorios/acordos?termo=21')
         
        elem = self.browser.find_element_by_css_selector('div#content.colM h1')
        self.assertTrue(elem.text.find('13/11711-5') >= 0)
        
        elem = self.browser.find_element_by_css_selector('tr#tr_1_2.nivel1 td')
        self.assertTrue(elem.text.find(u'Colaboração') >= 0)
        
        elem = self.browser.find_element_by_css_selector('.nivel3 td a')
        logger.debug(elem.text)

class RedeTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(RedeTest, self).setUp()
        
    def tearDown(self):
        super(RedeTest, self).tearDown()
    
    def test_bloco_ip_lista(self):
        req = self.browser.get(self.sistema_url + '/admin/rede/blocoip/')
        self.assertFalse(self.is_http_500(), u'Requisicao retornou HTTP (500)')
        self.assertFalse(self.is_http_404(), u'Requisicao retornou HTTP (404)')
